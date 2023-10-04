import logging, os, datetime

def get_logger(name):
    # keeping track of working directory
    cwd = os.getcwd()
    file_loc = os.path.abspath(__file__)
    file_dir = os.path.dirname(file_loc)
    os.chdir(file_dir)
    
    now_time = datetime.datetime.now()
    s_time = now_time.strftime('%y_%m_%d__%H_%M_%S')
    f_name = "log/CPS_" + s_time + ".log"
    log_format = '%(asctime)s %(name)8s %(levelname)5s %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename=f_name,
                        filemode='w')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(handler)

    os.chdir(cwd) # returning context of workdir
    return logging.getLogger(name)