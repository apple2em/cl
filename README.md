# cl

A workspace repository managed with Claude Code and oh-my-claudecode.

## Setup

```bash
git clone https://github.com/apple2em/cl.git
cd cl
```

## Tools

### todo.py — CLI Todo Manager

Todos are stored in `~/.cl_todos.json`.

```bash
python todo.py add Buy groceries       # add a todo
python todo.py list                    # show pending todos
python todo.py list --all              # show all todos
python todo.py list --done             # show completed todos
python todo.py done <id>               # mark a todo as done
python todo.py remove <id>             # delete a todo
python todo.py clear                   # remove all completed todos
```
