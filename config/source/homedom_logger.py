import logging


def set_logger(log_name, log_level):
    logging.basicConfig(level=log_level,
                        format='%(asctime)s - {} - %(name)s - %(levelname)s - %(message)s'.format(log_name),
                        datefmt='%m-%d %H:%M:%S',
                        filename='/var/log/homedom/{}.log'.format(log_name),
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s - {} - %(name)s - %(levelname)s - %(message)s'.format(log_name))
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
