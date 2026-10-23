---
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Quero adicionar uma rota de API `POST /tags` no módulo de tags que
cria uma etiqueta com nome (obrigatório, até 30 caracteres, único) e
cor em hexadecimal (opcional, padrão `#808080`). Nome repetido devolve
erro. Só o usuário autenticado cria tags. Os requisitos estão
completos: não precisa me perguntar nada antes de escrever a spec, os
casos de teste e o plano. Pare na confirmação do plano.
