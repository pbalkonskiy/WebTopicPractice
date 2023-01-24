#define _CRT_SECURE_NO_WARNINGS

#include <winsock2.h>

#include <iostream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <algorithm>

using namespace std;


void ErrorLog(string str, SOCKET soc) {
	cout << endl << str << endl;
	closesocket(soc);
	WSACleanup();

	system("pause");
	exit(0);
}


int main() {

	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);


	WORD wVersionRequested;
	WSADATA wsaData;
	wVersionRequested = MAKEWORD(2, 2);

	if (WSAStartup(wVersionRequested, &wsaData) != 0) {
		WSACleanup();
		system("pause");
		return 0;
	}

	SOCKET soc = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (soc == INVALID_SOCKET) {
		ErrorLog("Не удалось проинициализировать серверный сокет.\n", soc);
	}

	int port = 2000;
	struct sockaddr_in local;
	local.sin_family = AF_INET;
	local.sin_port = htons(port);
	local.sin_addr.s_addr = htonl(INADDR_ANY);

	while (true) {
		if (bind(soc, (struct sockaddr*)&local, sizeof(local)) != 0) {
			port++;
			local.sin_port = htons(port);
		}
		else {
			break;
		}
	}

	if (listen(soc, 5) != 0) {
		ErrorLog("Не удалось установить соединение со стороны сервера.\n", soc);
	}

	struct sockaddr_in remote_addr;
	int size = sizeof(remote_addr);

	SOCKET soc_cl = accept(soc, (struct sockaddr*)&remote_addr, &size);
	if (soc_cl == INVALID_SOCKET) {
		ErrorLog("Не удалось установить подключение со стороны сервера.\n", soc_cl);
	}

	char buffer[255];
	while (recv(soc_cl, buffer, sizeof(buffer), 0) != 0) {

		if (strcmp(buffer, "exit()") == 0) {
			cout << "Соединение закрыто клиентом." << endl;
			cout << "Завершение программы.\n" << endl;
			break;
		}

		for (int i = 0; i < strlen(buffer); i++) {
			for (int j = 0; j < (strlen(buffer) - 1); j++) {
				if (buffer[j] > buffer[j + 1]) {
					char symbol = buffer[j];
					buffer[j] = buffer[j + 1];
					buffer[j + 1] = symbol;
				}
			}
		}

		if (send(soc_cl, buffer, sizeof(buffer), 0) == SOCKET_ERROR) {
			ErrorLog("Не удалось отправить данные клиенту.\n", soc_cl);
		}
	}

	closesocket(soc_cl);
	WSACleanup();

	system("pause");
	return 0;

}