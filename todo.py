#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.expanduser("~"), ".cl_todos.json")


def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def cmd_add(args):
    todos = load()
    todo = {
        "id": (max((t["id"] for t in todos), default=0) + 1),
        "text": " ".join(args.text),
        "done": False,
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    todos.append(todo)
    save(todos)
    print(f"Added #{todo['id']}: {todo['text']}")


def cmd_list(args):
    todos = load()
    if args.all:
        filtered = todos
    elif args.done:
        filtered = [t for t in todos if t["done"]]
    else:
        filtered = [t for t in todos if not t["done"]]

    if not filtered:
        print("No todos found.")
        return

    for t in filtered:
        status = "x" if t["done"] else " "
        print(f"[{status}] #{t['id']}  {t['text']}")


def cmd_done(args):
    todos = load()
    matched = [t for t in todos if t["id"] == args.id]
    if not matched:
        print(f"No todo with id {args.id}.")
        sys.exit(1)
    matched[0]["done"] = True
    save(todos)
    print(f"Marked #{args.id} as done.")


def cmd_remove(args):
    todos = load()
    remaining = [t for t in todos if t["id"] != args.id]
    if len(remaining) == len(todos):
        print(f"No todo with id {args.id}.")
        sys.exit(1)
    save(remaining)
    print(f"Removed #{args.id}.")


def cmd_clear(args):
    todos = [t for t in load() if not t["done"]]
    save(todos)
    print("Cleared all completed todos.")


def main():
    parser = argparse.ArgumentParser(prog="todo", description="Simple todo manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", nargs="+", help="Todo text")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List todos")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Show all todos")
    group.add_argument("--done", action="store_true", help="Show only completed todos")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark a todo as done")
    p_done.add_argument("id", type=int, help="Todo ID")
    p_done.set_defaults(func=cmd_done)

    p_remove = sub.add_parser("remove", help="Remove a todo")
    p_remove.add_argument("id", type=int, help="Todo ID")
    p_remove.set_defaults(func=cmd_remove)

    p_clear = sub.add_parser("clear", help="Remove all completed todos")
    p_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
