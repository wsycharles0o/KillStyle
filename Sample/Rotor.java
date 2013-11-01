// This is a SUGGESTED skeleton file.  Throw it away if you don't use it.
package enigma;

/** Class that represents a rotor in the enigma machine.
 *  @author 
 */
class Rotor {
    // This needs other methods, fields, and constructors.

    private final String fwd;
    private final String bwd;
    private final String not;
    
    /** Size of alphabet used for plaintext and ciphertext. */
    static final int ALPHABET_SIZE = 26;

    public Rotor(String forward, String backward, String notch){
        fwd = forward;
        bwd = backward;
        not = notch;
    }
    
    /** Assuming that P is an integer in the range 0..25, returns the
     *  corresponding upper-case letter in the range A..Z. */
    static char toLetter(int p) {
        return (char) (p + (int) 'A');
    }

    /** Assuming that C is an upper-case letter in the range A-Z, return the
     *  corresponding index in the range 0..25. Inverse of toLetter. */
    static int toIndex(char c) {
        return ((int) c - (int) 'A');
    }

    /** Returns true iff this rotor has a ratchet and can advance. */
    boolean advances() {
        return true;
    }

    /** Returns true iff this rotor has a left-to-right inverse. */
    boolean hasInverse() {
        return true;
    }

    /** Return my current rotational setting as an integer between 0
     *  and 25 (corresponding to letters 'A' to 'Z').  */
    int getSetting() {
        return _setting;
    }

    /** Set getSetting() to POSN.  */
    void set(int posn) {
        assert 0 <= posn && posn < ALPHABET_SIZE;
        _setting = posn;
    }

    /** Return the conversion of P (an integer in the range 0..25)
     *  according to my permutation. */
    int convertForward(int p) {
        p = map(p);
        p = Rotor.toIndex(fwd.charAt(p));
        return demap(p);
    }

    /** Return the conversion of E (an integer in the range 0..25)
     *  according to the inverse of my permutation. */
    int convertBackward(int e) {
        e = map(e);
        e = Rotor.toIndex(bwd.charAt(e));
        return demap(e);
    }

    int map (int c) {
        c += _setting;
        c %= ALPHABET_SIZE;
        return c;
    }
    
    int demap (int c) {
        c -= _setting;
        if(c < 0)
            c += ALPHABET_SIZE;
        c %= ALPHABET_SIZE;
        return c;
    }
    
    /** Returns true iff I am positioned to allow the rotor to my left
     *  to advance. */
    boolean atNotch() {
            return (_setting == toIndex(not.charAt(0)) || 
                    (not.length() != 1 && _setting == toIndex(not.charAt(1))));
    }

    /** Advance me one position. */
    void advance() {
        _setting += 1;
        _setting %= ALPHABET_SIZE;
    }

    /** My current setting (index 0..25, with 0 indicating that 'A'
     *  is showing). */
    private int _setting;

}
