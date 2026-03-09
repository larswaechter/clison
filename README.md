# clison (wip)

CLI for beautifully printing JSON data in terminal.

<img src="https://github.com/larswaechter/clison/blob/main/preview.png?raw=true" width="80%">

## 📍 Introduction

--- project work in progress ---

## 🔨 Usage

Pipe JSON right into clison:

```bash
echo '[
    { "firstname": "Alice", "lastname": "Smith", "age": 30 },
    { "firstname": "Bob", "lastname": "Johnson", "age": 25 },
    { "firstname": "Charlie", "lastname": "Brown", "age": 35 }
]' | python -m clison.cli
```

or provide JSON from file:

```bash
 python -m clison.cli -f ./example.json
```
