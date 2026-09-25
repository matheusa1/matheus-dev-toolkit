---
description: Gera o esqueleto de um módulo novo seguindo Clean Architecture + DDD (domain/application/infra), convenções de nomenclatura T/I/E e injeção de dependência com Inversify. Use ao criar um módulo ou feature nova em um projeto TypeScript (NestJS, Next.js, React, React Native). Adapte os mesmos princípios de camadas quando o projeto não for TypeScript.
---

# Clean Architecture + DDD Scaffold

Objetivo: gerar a estrutura inicial de um módulo novo seguindo o padrão
`core/modules/<módulo>/{domain,application,infra}`.

## Antes de gerar

Confirme com o Matheus (ou com a spec/plano já aprovado):

1. Nome do módulo (em português ou inglês, conforme o resto do
   projeto).
2. Entidades principais do domínio.
3. Casos de uso (application) que esse módulo expõe.
4. Se precisa de persistência (TypeORM) e/ou exposição HTTP (NestJS
   controller).

## Estrutura a gerar

```
core/modules/<módulo>/
├── domain/
│   ├── entities/          # T<Entidade> — classes de domínio, sem dependência de framework
│   ├── ports/              # I<Repositorio>, I<Servico> — interfaces que a infra implementa
│   └── errors/              # E<Erro> — enums/erros de domínio
├── application/
│   ├── use-cases/          # um caso de uso por arquivo, depende só de domain (via ports)
│   └── dtos/                # T<Dto>Input / T<Dto>Output
├── infra/
│   ├── repositories/        # implementação concreta dos ports (TypeORM, Data Mapper)
│   ├── http/                 # controller NestJS, se aplicável
│   └── container-module.ts   # ContainerModule do Inversify deste módulo
```

## Convenções de nomenclatura

- `T` prefixa types/classes de dados (`TUser`, `TPedidoInput`).
- `I` prefixa interfaces/ports (`IUserRepository`).
- `E` prefixa enums (`EPedidoStatus`).

## Idioma e SOLID

- Todo o código gerado (nomes de arquivos, classes, métodos, tipos,
  comentários) em inglês.
- Respeite SOLID: uma responsabilidade por classe (um use case por
  arquivo), dependências sempre via interfaces `I*`, interfaces
  pequenas e focadas por port. Ver `using-dev-methodology`.

## Injeção de dependência (Inversify)

- Cada módulo tem seu próprio `ContainerModule` em
  `infra/container-module.ts`, registrado no container global da
  aplicação.
- Bindings são `singleton` compartilhado por padrão, salvo razão
  específica para transient/request-scoped.
- Um módulo pode depender de bindings de outro módulo através do
  container global — não crie acoplamento direto de import entre
  módulos além das interfaces de domínio.

## Persistência (quando houver TypeORM)

- Prefira o padrão **Data Mapper**: a entidade de domínio (`T*`) fica
  livre de decorators do TypeORM; um mapper na camada infra traduz
  entre a entidade TypeORM e a entidade de domínio. Isso evita modelos
  de domínio anêmicos acoplados ao ORM.

## Depois de gerar

- Não gere lógica de negócio "de exemplo" nos casos de uso — deixe os
  arquivos com a assinatura e um TODO, e siga para `test-driven-development`
  para implementar de fato caso a caso.
- Se o projeto não for TypeScript, aplique o mesmo princípio de camadas
  (domínio isolado → application → infra) usando os mecanismos de DI e
  nomenclatura idiomáticos da linguagem/framework em questão, e diga
  explicitamente que adaptou a convenção.
