from jhand import create_app, config

app = create_app(config=config.ProductionConfig)

if __name__ == '__main__':
    app.run()
