/*=============================================================================|
|  PROJECT SNAP7                                                         1.4.0 |
|==============================================================================|
|  Copyright (C) 2013, 2014 Davide Nardella                                    |
|  All rights reserved.                                                        |
|==============================================================================|
|  SNAP7 is free software: you can redistribute it and/or modify               |
|  it under the terms of the Lesser GNU General Public License as published by |
|  the Free Software Foundation, either version 3 of the License, or           |
|  (at your option) any later version.                                         |
|                                                                              |
|  It means that you can distribute your commexitial software linked with       |
|  SNAP7 without the requirement to distribute the soexite code of your         |
|  application and without the requirement that your application be itself     |
|  distributed under LGPL.                                                     |
|                                                                              |
|  SNAP7 is distributed in the hope that it will be useful,                    |
|  but WITHOUT ANY WARRANTY; without even the implied warranty of              |
|  MexitHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               |
|  Lesser GNU General Public License for more details.                         |
|                                                                              |
|  You should have received a copy of the GNU General Public License and a     |
|  copy of Lesser GNU General Public License along with Snap7.                 |
|  If not, see  http://www.gnu.org/licenses/                                   |
|==============================================================================|
|                                                                              |
|  New Server Example (1.1.0)                                                  |
|  Here we set ReadEventCallback to get in advance which area the client needs |
|  then we fill this area with a counter.                                      |
|  The purpose is to show how to modify an area before it be trasferred to the |
|  client                                                                      |
|                                                                              |
|=============================================================================*/
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include "snap7.h"
#include <iostream>
#include <fstream>
#include <sqlite3.h>
#include <string>
#include <inttypes.h>

TS7Server *Server;
unsigned char DB21[512];  // Our DB1
unsigned char DB103[1280];  // Our DB2
unsigned int DB3[1024]; // Our DB3
unsigned char OB1[1024]; // Our OB1
byte cnt = 0;
std::ofstream outfile;

// Here we use the callback to show the log, this is not the best choice since
// the callback is synchronous with the client access, i.e. the server cannot
// handle futher request from that client until the callback is complete.
// The right choice is to use the log queue via the method PickEvent.

void S7API EventCallBack(void *usrPtr, PSrvEvent PEvent, int Size)
{
	// print the event
	std::string myString = SrvEventText(PEvent).c_str();
	printf("%s\n", SrvEventText(PEvent).c_str());


	//db write
	if (PEvent->EvtParam1 == S7AreaDB)
	{

		// EvtParam2 contains the DB number.
		//DB21 contains the state of MV001
		switch (PEvent->EvtParam2)
		{
		case 21 :
		{
			//print the value
			printf("write value: %s in DB %s\n", std::to_string(PEvent->EvtParam4).c_str(), std::to_string(PEvent->EvtParam2).c_str());

			sqlite3 * db;
			int exit = 0;
			exit = sqlite3_open("../../../../waterTower/swat_s1_db.sqlite", &db);

			if (exit)
			{
				std::cerr << "Error open DB " << sqlite3_errmsg(db) << std::endl;
				memset(&DB3, ++cnt, sizeof(DB3));
			}
			else // query to the db with the water level value
			{
				std::cout << "Opened Database Successfully!" << std::endl;

				char *zErrMsg = 0;

				std::string strQuery = "UPDATE swat_s1 SET value=" + std::to_string(PEvent->EvtParam4) + " WHERE name='MV001'";
				const char * query = strQuery.c_str();
				/* Execute SQL statement */
				exit = sqlite3_exec(db, query, 0, 0, &zErrMsg);

				if (exit != SQLITE_OK ) {
					printf("SQL error: %s\n", zErrMsg);
					sqlite3_free(zErrMsg);
				} else {
					printf("Operation done successfully\n");
				}

			}
			//finally close db connection
			sqlite3_close(db);
			break;
		}

		//DB21 contains the state of P201
		case 103 :
		{
			//print the value
			printf("write value: %s in DB %s\n", std::to_string(PEvent->EvtParam4).c_str(), std::to_string(PEvent->EvtParam2).c_str());

			sqlite3 * db;
			int exit = 0;
			exit = sqlite3_open("../../../../waterTower/swat_s1_db.sqlite", &db);

			if (exit)
			{
				std::cerr << "Error open DB " << sqlite3_errmsg(db) << std::endl;
				memset(&DB3, ++cnt, sizeof(DB3));
			}
			else // query to the db with the water level value
			{
				std::cout << "Opened Database Successfully!" << std::endl;

				char *zErrMsg = 0;

				std::string strQuery = "UPDATE swat_s1 SET value=" + std::to_string(PEvent->EvtParam4) + " WHERE name='P201'";
				const char * query = strQuery.c_str();
				/* Execute SQL statement */
				exit = sqlite3_exec(db, query, 0, 0, &zErrMsg);

				if (exit != SQLITE_OK ) {
					printf("SQL error: %s\n", zErrMsg);
					sqlite3_free(zErrMsg);
				} else {
					printf("Operation done successfully\n");
				}

			}
			//finally close db connection
			sqlite3_close(db);
			break;
		}

		default: break;
		}
	}

	// save to log file
	std::ofstream log("s7comm.log", std::ios_base::app | std::ios_base::out);
	log << myString;
	log << "\n";
};

//	callback called by the sqlite3_exec() method before the read operation
static int callback(void *data, int argc, char **argv, char **azColName) {
	int i;
	fprintf(stderr, "%s: ", (const char*)data);

	for (int i = 0; i < argc; i++) {
		printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
		std::string value(argv[i]);
		std::cout << value << std::endl;
		int waterLevel = std::stof(value) * 1500;
		std::cout << waterLevel << std::endl;
		uint32_t endian = waterLevel;
		uint32_t swapEndian = __builtin_bswap32(endian);
		DB3[0] = swapEndian;
		//memset(&DB3, waterLevel, sizeof(DB3));
	}

	printf("\n");
	return 0;
}

static int valveReadCallback(void *data, int argc, char **argv, char **azColName) {
	int i;
	fprintf(stderr, "%s: ", (const char*)data);

	for (int i = 0; i < argc; i++) {
		printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
		std::string value(argv[i]);
		std::cout << value << std::endl;
		int valveState = std::stoi(value);
		if (data == "DB21")
			DB21[0] = valveState;
		else if (data =="DB103")
			DB103[0] = valveState;
	}
	return 0;
}

// The read event callback is called multiple times in presence of multiread var request
void S7API ReadEventCallBack(void *usrPtr, PSrvEvent PEvent, int Size)
{
	// print the read event
	printf("%s\n", SrvEventText(PEvent).c_str());
	if (PEvent->EvtParam1 == S7AreaDB)
	{
		// As example the DB requested is filled before transferred
		// EvtParam1 contains the DB number.
		switch (PEvent->EvtParam2)
		{
		case 21 :
		{
			sqlite3 * db;
			int exit = 0;
			exit = sqlite3_open("../../../../waterTower/swat_s1_db.sqlite", &db);

			if (exit)
			{
				std::cerr << "Error open DB " << sqlite3_errmsg(db) << std::endl;
				memset(&DB21, ++cnt, sizeof(DB21)); break;
			}
			else // query to the db with the water level value
			{
				std::cout << "Opened Database Successfully!" << std::endl;

				const char* data = "DB21";
				char *zErrMsg = 0;

				char *query = "SELECT value FROM swat_s1 WHERE name='MV001'";
				/* Execute SQL statement */
				exit = sqlite3_exec(db, query, valveReadCallback, (void*)data, &zErrMsg);

				if (exit != SQLITE_OK ) {
					printf("SQL error: %s\n", zErrMsg);
					sqlite3_free(zErrMsg);
				} else {
					printf("Operation done successfully\n");
				}

			}
			//finally close db connection
			sqlite3_close(db);
			break;
		}
		case 103 :
		{
			sqlite3 * db;
			int exit = 0;
			exit = sqlite3_open("../../../../waterTower/swat_s1_db.sqlite", &db);

			if (exit)
			{
				std::cerr << "Error open DB " << sqlite3_errmsg(db) << std::endl;
				memset(&DB103, ++cnt, sizeof(DB103)); break;
			}
			else // query to the db with the water level value
			{
				std::cout << "Opened Database Successfully!" << std::endl;

				const char* data = "DB103";
				char *zErrMsg = 0;

				char *query = "SELECT value FROM swat_s1 WHERE name='P201'";
				/* Execute SQL statement */
				exit = sqlite3_exec(db, query, valveReadCallback, (void*)data, &zErrMsg);

				if (exit != SQLITE_OK ) {
					printf("SQL error: %s\n", zErrMsg);
					sqlite3_free(zErrMsg);
				} else {
					printf("Operation done successfully\n");
				}

			}
			//finally close db connection
			sqlite3_close(db);
			break;
		}
		//if the db is available db3 contains the water level, otherwise we keep the usual behaviour
		case 3 :
		{
			sqlite3 * db;
			int exit = 0;
			exit = sqlite3_open("../../../../waterTower/swat_s1_db.sqlite", &db);

			if (exit)
			{
				std::cerr << "Error open DB " << sqlite3_errmsg(db) << std::endl;
				memset(&DB3, ++cnt, sizeof(DB3));
			}
			else // query to the db with the water level value
			{
				std::cout << "Opened Database Successfully!" << std::endl;

				const char* data = "Callback function called";
				char *zErrMsg = 0;

				char *query = "SELECT value FROM swat_s1 WHERE name='LIT101'";
				/* Execute SQL statement */
				exit = sqlite3_exec(db, query, callback, (void*)data, &zErrMsg);

				if (exit != SQLITE_OK ) {
					printf("SQL error: %s\n", zErrMsg);
					sqlite3_free(zErrMsg);
				} else {
					printf("Operation done successfully\n");
				}

			}
			//finally close db connection
			sqlite3_close(db);
			break;
		}

		case 4 : memset(&OB1, ++cnt, sizeof(OB1)); break;
		}
	}
};

int main(int argc, char* argv[])
{
	int Error;
	Server = new TS7Server;

	// Share some resoexites with our virtual PLC
	Server->RegisterArea(srvAreaDB,      // We are registering a DB
	                     21,             // Its number is 1 (DB1)
	                     &DB21,          // Our buffer for DB1
	                     sizeof(DB21));  // Its size
	// Do the same for DB2 and DB3
	Server->RegisterArea(srvAreaDB, 103, &DB103, sizeof(DB103));
	Server->RegisterArea(srvAreaDB, 3, &DB3, sizeof(DB3));
	Server->RegisterArea(srvAreaOB, 1, &OB1, sizeof(OB1));

	// We mask the read event to avoid the double trigger for the same event
	Server->SetEventsMask(~evcDataRead);
	Server->SetEventsCallback(EventCallBack, NULL);
	// Set the Read Callback
	Server->SetReadEventsCallback(ReadEventCallBack, NULL);
	// Start the server onto the default adapter.
	// To select an adapter we have to use Server->StartTo("192.168.x.y").
	// Start() is the same of StartTo("0.0.0.0");
	Error = Server->StartTo(argv[1]);
	if (Error == 0)
	{
		// Now the server is running ... wait a key to terminate
		getchar();
		printf("%s\n", "Bye!");
	}
	else
		printf("%s\n", SrvErrorText(Error).c_str());

	// If you got a start error:
	// Windows - most likely you ar running the server in a pc on wich is
	//           installed step 7 : open a command prompt and type
	//             "net stop s7oiehsx"    (Win32) or
	//             "net stop s7oiehsx64"  (Win64)
	//           And after this test :
	//             "net start s7oiehsx"   (Win32) or
	//             "net start s7oiehsx64" (Win64)
	// Unix - you need root rights :-( because the isotcp port (102) is
	//        low and so it's considered "privileged".

	Server->Stop(); // <- not strictly needed, every server is stopped on deletion
	//    and every client is gracefully disconnected.
	delete Server;
}

// Finally, this is a very minimalist (but working) server :
/*
int main(int argc, char* argv[])
{
   TS7Server *Server = new TS7Server;
   Server->Start();
   getchar();
   delete Server;
}
*/