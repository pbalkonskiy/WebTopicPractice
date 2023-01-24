#define _CRT_SECURE_NO_WARNINGS
#define _WINSOCK_DEPRECATED_NO_WARNINGS

#include <winsock2.h>

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <Windows.h>

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


	WORD wVersionRequired;
	WSADATA wsaData;
	wVersionRequired = MAKEWORD(2, 2);

	if (WSAStartup(wVersionRequired, &wsaData) != 0) {
		WSACleanup();
		system("pause");
		return 0;
	}

	SOCKET soc = socket(AF_INET, SOCK_STREAM, 0);
	if (soc == INVALID_SOCKET) {
		ErrorLog("Не удалось проинициализировать сокет со стороны клиента.\n", soc);
	}

	int port = 2000;
	struct sockaddr_in peer;
	peer.sin_family = AF_INET;
	peer.sin_port = htons(port);
	peer.sin_addr.s_addr = inet_addr("127.0.0.1");

	while (true) {
		if (connect(soc, (struct sockaddr*)&peer, sizeof(peer)) != 0) {
			port++;
			peer.sin_port = htons(port);
		}
		else {
			break;
		}
	}

	while (true) {
		char buffer[255], message[255];
		cout << "Сообщение серверу: " << endl;
		cin.getline(buffer, sizeof(buffer), '\n');

		if (send(soc, buffer, sizeof(buffer), 0) == INVALID_SOCKET) {
			ErrorLog("Не удалось отправить данные серверу.\n", soc);
		}

		if (strcmp(buffer, "exit()") == 0) {
			cout << "\nСоединение было закрыто клиентом." << endl;
			cout << "Завершение программы.\n" << endl;
			break;
		}

		if (recv(soc, message, sizeof(message), 0) != 0) {
			message[strlen(message)] = '\0';
			cout << "По алфавиту: " << message << "\n\n";
		}
	}

	closesocket(soc);
	WSACleanup();

	system("pause");
	return 0;
}