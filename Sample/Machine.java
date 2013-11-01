// This is a SUGGESTED skeleton file.  Throw it away if you don't use it.
package enigma;

/** Class that represents a complete enigma machine.
 *  @author Shengyu Wang
 */
class Machine {

    // This needs other methods or constructors.

    private Rotor[] r;
    
    public Machine() {
        r = new Rotor[5];
    }
    
    /** Set my rotors to (from left to right) ROTORS.  Initially, the rotor
     *  settings are all 'A'. */
    void replaceRotors(Rotor[] rotors) {
        r = rotors;
    }

    /** Set my rotors according to SETTING, which must be a string of four
     *  upper-case letters. The first letter refers to the leftmost
     *  rotor setting.  */
    void setRotors(String setting) {
        r[1].set(Rotor.toIndex(setting.charAt(0)));
        r[2].set(Rotor.toIndex(setting.charAt(1)));
        r[3].set(Rotor.toIndex(setting.charAt(2)));
        r[4].set(Rotor.toIndex(setting.charAt(3)));
    }

    /** Returns the encoding/decoding of MSG, updating the state of
     *  the rotors accordingly. */
    String convert(String msg) {
        int c;
        for(int i = 0; i < msg.length(); i++) {
            if(r[3].atNotch()){
                r[3].advance();
                r[2].advance();
            } else if(r[4].atNotch()) {
                r[3].advance();
            }
            r[4].advance();
            c = Rotor.toIndex(msg.charAt(i));
            c = r[4].convertForward(c);
            c = r[3].convertForward(c);
            c = r[2].convertForward(c);
            c = r[1].convertForward(c);
            c = r[0].convertForward(c);
            c = r[1].convertBackward(c);
            c = r[2].convertBackward(c);
            c = r[3].convertBackward(c);
            c = r[4].convertBackward(c);
            msg = msg.substring(0, i) + Rotor.toLetter(c) + msg.substring(i + 1);
        }
        return msg;
    }
}
