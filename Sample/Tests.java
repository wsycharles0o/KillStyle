package enigma;

public class Tests {

	/**
	 * @param args The test number
	 */
	public static void main(String[] args) {
		int s = 4;
		
		/*Rotor.toLetter*/
		if(s == 1 || s == 0) {
			test(Rotor.toLetter(0)=='A' && Rotor.toLetter(3)=='D' && Rotor.toLetter(25)=='Z', s);
		}
		
		/*Rotor.toIndex*/
		if(s == 2 || s == 0) {
		    test(Rotor.toIndex('A')==0 && Rotor.toIndex('D')==3 && Rotor.toIndex('Z')==25, s);
		}
		
		/*Main.checkLine*/
		if(s == 3 || s == 0){
            checkLine("abdsdf   dsdfaA SDF  ");
            checkLine("");
            checkLine("*NASDF ASDF");
            checkLine("ASDFJ jiji   D!");
            checkLine("**NASDF ASDF");
        }
		
	    /*char comparison*/
        if(s == 4 || s == 0){
            char i = 'A';
            test((i >= 'A' && i <= 'Z'), s);
        }
	}
	
    private static void errexit(){
        o("Error Exited\n");
    }
    
    private static void checkLine(String line) {
        if(!(line.matches("[*][A-Z ]*") || (line.matches("[A-Za-z \t]*")))) {
            errexit();
        }
    }
    
	public static void o(String i) {
	    System.out.print(i);
	}
	
	public static void passed(String i)	{
		o("Test " + i + " passed !!! \n");
	}
	
	public static void failed(String i)	{
	    o("Test " + i + " failed !!! \n");
	}
	
	public static void test(boolean t,int s)
	{
		if(t)
			passed(String.valueOf(s));
		else
			failed(String.valueOf(s));
	}
	
	
}
