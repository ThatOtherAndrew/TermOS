def main() -> None:
    from .termos import TermOS
    app_return = True
    while app_return is not None:
        app_return = TermOS().run()


if __name__ == '__main__':
    main()
