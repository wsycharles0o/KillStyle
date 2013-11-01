// This is a SUGGESTED skeleton file.  Throw it away if you want.
package enigma;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;


/** Enigma simulator.
 *  @author Shengyu Wang
 */
public final class Main {

    // WARNING: Not all methods that have code in them are complete!

    /** Process a sequence of encryptions and decryptions, as
     *  specified in the input from the standard input.  Print the
     *  results on the standard output. Exits normally if there are
     *  no errors in the input; otherwise with code 1. */
    public static void main(String[] unused) {
        Machine M;
        BufferedReader input =
            new BufferedReader(new InputStreamReader(System.in));
        buildRotors();

        M = null;

        try {
            while (true) {
                String line = input.readLine();
                if (line == null) {
                    break;
                }
                if (line.equals("")) {
                    System.out.print("\n");
                    continue;
                }
                checkLine(line);
                if (isConfigurationLine(line)) {
                    M = new Machine();
                    configure(M, line);
                } else {
                    if (M == null){
                        errexit();
                    }
                    printMessageLine(M.convert(standardize(line)));
                }
            }
        } catch (IOException excp) {
            System.err.printf("Input error: %s%n", excp.getMessage());
            System.exit(1);
        }
    }

    private static void errexit() {
        System.out.print("Error Exited!");//FIXME
        System.exit(1);
    }
    
    private static void checkLine(String line) {
        if(!(line.matches("[*][A-Z ]*") || (line.matches("[A-Za-z \t]*")))) {
            errexit();
        }
    }

    /** Return true iff LINE is an Enigma configuration line. */
    private static boolean isConfigurationLine(String line) {
        return line.charAt(0) == '*';
    }

    /** Configure M according to the specification given on CONFIG,
     *  which must have the format specified in the assignment. */
    private static void configure(Machine M, String config) {
        Rotor[] r = new Rotor[5];
        if(config.charAt(0) != '*' || config.charAt(1) != ' ') {
            errexit();
        }
        String[] param = config.substring(2).split(" ");
        if(param.length != 6 || (!param[5].matches("[A-Z]{4}"))) {
            errexit();
        }
        for(int ri = 0; ri < 5; ri++) {
            for(int ni = 0; ni < 12; ni++) {
                if(param[ri].equals(rname[ni])) {
                    r[ri] = rotors[ni];
                    break;
                }
                if(ni == 11) {
                    errexit();
                }
            }
        }
        M.replaceRotors(r);
        M.setRotors(param[5]);
    }

    /** Return the result of converting LINE to all upper case,
     *  removing all blanks and tabs.  It is an error if LINE contains
     *  characters other than letters and blanks. */
    private static String standardize(String line) {
        line = line.toUpperCase();
        String ans = "";
        for(int i = 0; i < line.length(); i++) {
            if(line.charAt(i) >= 'A' && line.charAt(i) <= 'Z')
                ans += line.charAt(i);
        }
        return ans;
    }

    /** Print MSG in groups of five (except that the last group may
     *  have fewer letters). */
    private static void printMessageLine(String msg) {
        if (msg.length()!=0) {
            System.out.print(msg.charAt(0));
            for(int i = 1; i< msg.length();i++) {
                if(i % 5 == 0) {
                    System.out.print(" ");
                }
                System.out.print(msg.charAt(i));
            }
        }
        System.out.print("\n");
    }

    private static Rotor[] rotors = new Rotor[12];
    private static String[] rname = new String[12];
    /** Create all the necessary rotors. */
    private static void buildRotors() {
        String[][] specs = PermutationData.ROTOR_SPECS;
        for (int i = 0; i < 8; i++) {
            rname[i] = specs[i][0];
            rotors[i] = new Rotor(specs[i][1], specs[i][2], specs[i][3]);
        }
        for (int i = 8; i < 10; i++) {
            rname[i] = specs[i][0];
            rotors[i] = new FixedRotor(specs[i][1], specs[i][2]);
        }
        for (int i = 10; i < 12; i++) {
            rname[i] = specs[i][0];
            rotors[i] = new Reflector(specs[i][1]);
        }
    }

}

