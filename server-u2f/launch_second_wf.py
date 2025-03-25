#!/usr/bin/env python3
from typing import Optional, Dict
from pathlib import Path
import subprocess
import pika
import time
import sys
import os

SCRIPT_DIR = (Path(__file__).parent).resolve()
WORKSPACE_DIR = (SCRIPT_DIR.parent.parent).resolve()

WORKFLOW_NAME = "second-wf.yml"
WORKFLOW_REPOSITORY = "ClementBrz/test-rabbitmq"

def run_cmd(cmd: str,
            cwd: Path = WORKSPACE_DIR,
            print_output: bool = False,
            no_throw: bool = False,
            env: Optional[Dict[str, str]] = None) -> str:
    print(f"[run_cmd] Running: {cmd} from {cwd}")

    ret = subprocess.run(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         universal_newlines=True,
                         cwd=cwd,
                         env=env)
    if no_throw is False and ret.returncode:
        print(f"[run_cmd] Error {ret.returncode} raised while running cmd: {cmd}")
        print("[run_cmd] Output was:")
        print(ret.stdout)
        raise ValueError()

    if print_output:
        print(f"[run_cmd] Output:\n{ret.stdout}")

    return ret.stdout.strip()


def launch_gh_workflow(ch, method, properties, body):
    data = body.decode()
    gh_cmd = f"echo '{data}' | gh workflow run -R {WORKFLOW_REPOSITORY} {WORKFLOW_NAME} \
                --json"
    run_cmd(gh_cmd)
    print(f"Command: {gh_cmd}: was successfully executed\n \
            Github Workflow: {WORKFLOW_NAME}: was triggered")


def main():
    time.sleep(5)
    print("entering launch_second_wf")
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.18.0.2'))
    print("connection created")
    channel = connection.channel()
    print("channel created")

    channel.queue_declare(queue='u2f_sign_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='u2f_sign_queue', on_message_callback=launch_gh_workflow)

    print(' Waiting for tasks. To exit press CTRL+C')
    channel.start_consuming()


if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('RabbitMQ worker manually interrupted!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")