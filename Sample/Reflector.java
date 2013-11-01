// This is a SUGGESTED skeleton file.  Throw it away if you don't use it.
package enigma;

/** Class that represents a reflector in the enigma.
 *  @author Shengyu Wang
 */
class Reflector extends Rotor {

    // This needs other methods or constructors.

    public Reflector(String forward) {
        super(forward, "@", "-999");
    }

    boolean hasInverse() {
        return false;
    }

    boolean atNotch() {
        return false;
    }
    
    /** Returns a useless value; should never be called. */
    int convertBackward(int unused) {
        throw new UnsupportedOperationException();
    }
    
    /** Does nothing; should never be called. */
    void advance() {
        throw new UnsupportedOperationException();
    }

}
