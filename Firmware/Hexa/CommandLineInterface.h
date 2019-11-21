/******************************************************************************
 * @File		CommandLineInterface.h
 * @Brief		The User Interface / Command Line Interface backend
 * @Date		13/11/2019 (Last Updated)
 * @Author(s)	William Bednall
 ******************************************************************************/
#ifndef CommandLineInterface_h
#define CommandLineInterface_h

const int maxCharCommand = 30;

struct cmdFormat {
	const String term;			//Leonardo = 6 bytes, ESP8266 = ? bytes
	void (*func)(void);			//Leonardo = 2 bytes, ESP8266 = 4 bytes
};

class CommandLineInterface {
	public:
		CommandLineInterface(Stream &targetSerial);
		void setup();
		void loop();

		void setSdkMode(bool toggle);

		void bind(const cmdFormat *cmdTable, uint16_t size);		//String Command			For example: "help"

		//Parameter to Value
		int			readInt();
		long		readLong();
		bool		readBool();
		float		readFloat();
		double		readDouble();
		char		readChar();
		String		readString();

	private:
		void resetBuffer();

		//Command mapping
		const cmdFormat *cmdUserBindings = NULL;	//Used to store location of command table
		uint16_t cmdUserSize;
		bool userCmd();

		//Parameter input stuff
		int separatorPos = 0;
		String paramHandle();

		//Variables
		Stream *refSerial;
		int countString = 0;
		char inputBuffer[maxCharCommand];
		char newChar;
		bool sdkMode;
};

extern CommandLineInterface CLI;

#endif
