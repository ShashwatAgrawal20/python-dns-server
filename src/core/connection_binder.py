def bind_connection(upd_socket, ip, port) -> None:
    """
    Bind the connection to the specified ip and port.

    Parameters:
    - upd_socket : The socket object to be bound.
    - ip : The IP to be bound.
    - port : The PORT to be bound.
    """
    try:
        upd_socket.bind((ip, port))
    except Exception as e:
        print("Error: ", e)
        exit(1)
