# Guia da atividade: CI/CD

## O que foi preparado

O arquivo `.github/workflows/ci.yml` executa, a cada push em qualquer branch e em pull requests para `main`:

1. Checkout e configuração do Python 3.14.
2. Instalação das dependências, lint e verificação de formatação com Ruff.
3. Testes unitários e de integração HTTP com cobertura combinada de linhas e ramificações de pelo menos 80%; os relatórios são guardados como artefatos do Actions.
4. Construção da imagem Docker e verificação de que a API inicia e disponibiliza o OpenAPI.
5. Apenas em push na `main`, depois que as duas verificações anteriores passarem, um deploy hook pede ao Render o deploy do commit validado.

A resposta de sucesso do hook confirma apenas que o deploy foi iniciado ou enfileirado, não que ficou disponível. Confira o resultado no Render. Cancelamentos de execuções antigas evitam trabalho desnecessário, mas o histórico do Render deve ser conferido em pushes próximos.

## Configurar o Render e o GitHub

1. Envie este projeto para o seu repositório GitHub. A configuração ainda está apenas na cópia local.
2. Crie no Render um **Web Service** conectado a esse repositório, branch `main`, usando runtime **Docker** e o Dockerfile da raiz. O primeiro deploy criado pelo Render é uma inicialização do serviço; para a demonstração, use um push posterior controlado pela pipeline.
3. Nas configurações do serviço, desative o deploy automático por alteração no repositório. Isso é indispensável para que o Render não publique uma alteração antes da CI passar. A API usa a porta informada por `PORT`.
4. Copie o Deploy Hook da página Settings do serviço. É uma credencial: não coloque seu valor no código, no relatório ou em prints.
5. No GitHub, acesse Settings → Secrets and variables → Actions → New repository secret. Crie `RENDER_DEPLOY_HOOK` com o valor completo do hook. O workflow acrescenta `&ref=<SHA>` ao hook padrão do Render, que já possui o parâmetro `key`.
6. Faça um novo push na `main`. Em Actions, abra a execução e confira qualidade, Docker e deploy. No Render, confirme que o deploy do mesmo commit terminou com status Live. Acesse `https://<seu-servico>.onrender.com/docs` e execute uma requisição de exemplo. Confira os custos, limites e disponibilidade do seu plano no Render.
7. Crie uma branch e um PR para `main`: a CI deve executar, mas o job de deploy deve ser ignorado. Para demonstrar bloqueio, introduza uma falha de teste em uma branch de demonstração e registre a falha; não mantenha a falha na versão final. Uma falha em um push para `main` também impediria o job de deploy.

O Render pode fazer deploy de um SHA específico a partir do hook; deixe o deploy automático do próprio Render desligado: https://render.com/docs/deploy-hooks

## Executar localmente

```bash
python -m pip install ".[dev]"
ruff check .
ruff format --check .
pytest --cov=app --cov-branch --cov-report=term-missing --cov-fail-under=80
```

Com Docker em funcionamento: `docker build -t api-estatistica .` e `docker run --rm -p 8000:8000 api-estatistica`.

## Relatório para o professor

O laboratório pede **um único PDF** contendo o link do repositório, o workflow, os prompts, alterações, análise e evidências. Registre fielmente cada interação relevante: prompt, resultado, problema, ajuste e quem o fez. Conte os prompts ao finalizar; não invente números nem evidências. Inclua capturas do Actions com jobs aprovados, do PR sem deploy, do Render com o SHA e status Live, e da API respondendo. O professor também pede que você informe alterações manuais e como validou a pipeline.

A sequência desta conversa inclui o pedido para analisar e corrigir a API e o pedido para criar a pipeline usando os materiais de aula, a skill Ponytail e o projeto de referência. Registre também as próximas interações e eventuais erros reais de configuração e correções.

## Limites

A cobertura de 80% é combinada entre as duas categorias de teste, não uma meta separada para cada categoria. Cobertura não garante correção. A etapa de deploy inicia o processo no Render, mas não acompanha seu término. Sem conta, secret, execução no GitHub e verificação do serviço, não é possível afirmar que o CD funciona de ponta a ponta.
