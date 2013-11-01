package enigma;

/** Class that represents a rotor that has no ratchet and does not advance.
 *  @author Shengyu Wang
 */
class FixedRotor extends Rotor {

    // This needs other methods or constructors.

    public FixedRotor(String forward, String backward) {
        super(forward, backward, "-999");
    }
    
    boolean atNotch() {
        return false;
    }
    
    /** Does nothing; should never be called. */
    void advance() {
        throw new UnsupportedOperationException();
    }

}
