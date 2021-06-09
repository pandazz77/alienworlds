title = """
      __          ___           _       __      ____ _  _   
     /\ \        / / |         | |      \ \    / / /| || |  
    /  \ \  /\  / /| |__   ___ | |_ _____\ \  / / /_| || |_ 
   / /\ \ \/  \/ / | '_ \ / _ \| __|______\ \/ / '_ \__   _|
  / ____ \  /\  /  | |_) | (_) | |_        \  /| (_) | | |  
 /_/    \_\/  \/   |_.__/ \___/ \__|        \/  \___(_)|_|  
                                                            """

def print_info(config):
    cfg_info = "Your config:\n"
    for key, value in config.items():
        cfg_info +="    "+str(key)+" = "+str(value)+"\n"
    print(title+"\n\n\n")
    print(cfg_info)