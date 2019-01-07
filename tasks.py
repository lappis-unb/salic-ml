from invoke import task


@task
def hello(ctx, name='world'):
    ctx.run(f'echo "hello {name}"')