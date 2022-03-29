import socket as sc
import time
from collections import namedtuple


def main():

    run_server = True
    with open('log.txt', 'w') as log_file:

        # Bind a socket to a port
        server_address = ('localhost', 9090)
        sock = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
        sock.bind(server_address)

        # Listening for incoming connections
        sock.listen(1)

        while run_server:

            # if there is a glitch or something goes wrong, we must always close the connection,
            # so use the try-finally mapping to do this
            try:
                # Waiting for connection
                connection, client_address = sock.accept()
                while True:

                    # Accepting data
                    data = connection.recv(23)

                    # if we receive any data, we process it
                    if data:

                        # If we accept the "stop" command, we stop the server.
                        if b'stop' in data:
                            run_server = False
                            break

                        # If a "bye" command is received, close the current connection
                        # and wait for the next client to connect.
                        if b'bye' in data:
                            break

                        if len(data) == 23:
                            data_parse = namedtuple('Decode', 'Participant_number Channel_id Time Group_number')._make(data.decode().split())
                            if data_parse.Group_number == '00':
                                print(f'спортсмен, нагрудный номер {data_parse.Participant_number} '
                                       f'прошёл отсечку {data_parse.Channel_id} в "{ data_parse.Time:.5}"')

                            # write all data to the log file
                            log_file.write(time.strftime("%c") + ' --- ' + data.decode() + '\n')

                # Clear the connection and close the file
            finally:
                connection.close()


if __name__ == "__main__":
    main()
