# HopServer

HopServer is a simple, lightweight web server written in Python. It was built to be easy to use and understand, making it a great starting point for learning about web servers and HTTP request handling.

## Features

*   **Static File Serving**: Serve any file from the server's directory.
*   **Directory Listing**: If you request a directory that doesn't have an `index.html` file, it will list the contents of the directory.
*   **CGI Script Execution**: The server can execute Python scripts (`.py` files) and return their output.
*   **Customizable Request Handling**: The server uses a case-based approach to handle requests, which can be easily extended to add new functionality.
*   **Error Handling**: The server provides informative error pages for common issues like missing files.

## How to Run

1.  Make sure you have Python 3 installed.
2.  Open your terminal and navigate to the project directory.
3.  Run the server with the following command:

    ```bash
    python server.py
    ```

4.  The server will start on port 7000. You can access it by opening your web browser and navigating to `http://localhost:7000`.

## Usage

*   **Accessing Files**: To access a file, simply navigate to its path in your browser. For example, to view the `index.html` file, go to `http://localhost:7000/index.html`.
*   **Directory Listing**: To see a directory listing, navigate to the directory's path. For example, `http://localhost:7000/`.
*   **CGI Scripts**: To execute a Python script, navigate to its path. For example, if you have a `hello.py` script, you can run it by going to `http://localhost:7000/hello.py`.

## Project Structure

*   `server.py`: The main entry point for the server. It creates an `HTTPServer` and uses the `RequestHandler` to handle requests.
*   `request_handler.py`: This file contains the `RequestHandler` class, which defines how to handle `GET` requests. It uses a list of "cases" to decide how to respond to a request.
*   `cases.py`: This file defines the different "cases" for handling requests. Each case has a `test` method to see if it applies to the current request and an `act` method to handle the request.
*   `index.html`: A sample HTML file that is served by default.
*   `consider.md`: Contains some notes and considerations about the server's implementation.

## Dependencies

This project uses only standard Python libraries, so there are no external dependencies to install.

## Limitations

*   The server reads the entire content of a file into memory before serving it. This can be an issue when dealing with very large files.
*   The server is single-threaded and can only handle one request at a time.