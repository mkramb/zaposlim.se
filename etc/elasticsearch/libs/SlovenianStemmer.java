// This file was generated automatically by the Snowball to Java compiler

package org.tartarus.snowball.ext;

import org.tartarus.snowball.Among;

 /**
  * This class was automatically generated by a Snowball to Java compiler 
  * It implements the stemming algorithm defined by a snowball script.
  */

public class SlovenianStemmer extends org.tartarus.snowball.SnowballProgram {

private static final long serialVersionUID = 1L;

        private final static SlovenianStemmer methodObject = new SlovenianStemmer ();

                private final static Among a_0[] = {
                    new Among ( "anski", -1, 1, "", methodObject ),
                    new Among ( "evski", -1, 1, "", methodObject ),
                    new Among ( "ovski", -1, 1, "", methodObject )
                };

                private final static Among a_1[] = {
                    new Among ( "stvo", -1, 1, "", methodObject ),
                    new Among ( "\u00C2\u00B9tvo", -1, 1, "", methodObject )
                };

                private final static Among a_2[] = {
                    new Among ( "ega", -1, 1, "", methodObject ),
                    new Among ( "ija", -1, 1, "", methodObject ),
                    new Among ( "ila", -1, 1, "", methodObject ),
                    new Among ( "ema", -1, 1, "", methodObject ),
                    new Among ( "vna", -1, 1, "", methodObject ),
                    new Among ( "ite", -1, 1, "", methodObject ),
                    new Among ( "ste", -1, 1, "", methodObject ),
                    new Among ( "\u00C2\u00B9\u00C3\u00A8e", -1, 1, "", methodObject ),
                    new Among ( "ski", -1, 1, "", methodObject ),
                    new Among ( "\u00C2\u00B9ki", -1, 1, "", methodObject ),
                    new Among ( "iti", -1, 1, "", methodObject ),
                    new Among ( "ovi", -1, 1, "", methodObject ),
                    new Among ( "\u00C3\u00A8ek", -1, 1, "", methodObject ),
                    new Among ( "ovm", -1, 1, "", methodObject ),
                    new Among ( "\u00C3\u00A8an", -1, 1, "", methodObject ),
                    new Among ( "len", -1, 1, "", methodObject ),
                    new Among ( "ven", -1, 1, "", methodObject ),
                    new Among ( "\u00C2\u00B9en", -1, 1, "", methodObject ),
                    new Among ( "ejo", -1, 1, "", methodObject ),
                    new Among ( "ijo", -1, 1, "", methodObject ),
                    new Among ( "ast", -1, 1, "", methodObject ),
                    new Among ( "ost", -1, 1, "", methodObject )
                };

                private final static Among a_3[] = {
                    new Among ( "ja", -1, 1, "", methodObject ),
                    new Among ( "ka", -1, 1, "", methodObject ),
                    new Among ( "ma", -1, 1, "", methodObject ),
                    new Among ( "ec", -1, 1, "", methodObject ),
                    new Among ( "je", -1, 1, "", methodObject ),
                    new Among ( "eg", -1, 1, "", methodObject ),
                    new Among ( "eh", -1, 1, "", methodObject ),
                    new Among ( "ih", -1, 1, "", methodObject ),
                    new Among ( "mi", -1, 1, "", methodObject ),
                    new Among ( "ti", -1, 1, "", methodObject ),
                    new Among ( "ij", -1, 1, "", methodObject ),
                    new Among ( "al", -1, 1, "", methodObject ),
                    new Among ( "il", -1, 1, "", methodObject ),
                    new Among ( "em", -1, 1, "", methodObject ),
                    new Among ( "om", -1, 1, "", methodObject ),
                    new Among ( "an", -1, 1, "", methodObject ),
                    new Among ( "en", -1, 1, "", methodObject ),
                    new Among ( "in", -1, 1, "", methodObject ),
                    new Among ( "do", -1, 1, "", methodObject ),
                    new Among ( "jo", -1, 1, "", methodObject ),
                    new Among ( "ir", -1, 1, "", methodObject ),
                    new Among ( "at", -1, 1, "", methodObject ),
                    new Among ( "ev", -1, 1, "", methodObject ),
                    new Among ( "iv", -1, 1, "", methodObject ),
                    new Among ( "ov", -1, 1, "", methodObject ),
                    new Among ( "o\u00C3\u00A8", -1, 1, "", methodObject )
                };

                private final static Among a_4[] = {
                    new Among ( "a", -1, 1, "", methodObject ),
                    new Among ( "c", -1, 1, "", methodObject ),
                    new Among ( "e", -1, 1, "", methodObject ),
                    new Among ( "i", -1, 1, "", methodObject ),
                    new Among ( "m", -1, 1, "", methodObject ),
                    new Among ( "o", -1, 1, "", methodObject ),
                    new Among ( "u", -1, 1, "", methodObject ),
                    new Among ( "\u00C2\u00B9", -1, 1, "", methodObject )
                };

                private final static Among a_5[] = {
                    new Among ( "a", -1, 1, "", methodObject ),
                    new Among ( "e", -1, 1, "", methodObject ),
                    new Among ( "i", -1, 1, "", methodObject ),
                    new Among ( "o", -1, 1, "", methodObject ),
                    new Among ( "u", -1, 1, "", methodObject )
                };

                private static final char g_crke[] = {255, 255, 62, 2, 0, 0, 0, 0, 0, 0, 0, 33, 0, 0, 0, 0, 128 };

                private static final char g_samoglasniki[] = {17, 65, 16 };

                private static final char g_soglasniki[] = {119, 95, 23, 1, 0, 0, 0, 0, 0, 0, 128, 16, 0, 0, 0, 0, 64 };

        private int I_p1;

                private void copy_from(SlovenianStemmer other) {
                    I_p1 = other.I_p1;
                    super.copy_from(other);
                }

                public boolean stem() {
            int among_var;
            int v_1;
            int v_2;
            int v_3;
            int v_4;
            int v_5;
            int v_6;
            int v_7;
            int v_8;
            int v_9;
            int v_10;
                    // (, line 27
                    I_p1 = limit;
                    // backwards, line 30
                    limit_backward = cursor; cursor = limit;
                    // (, line 30
                    // do, line 31
                    v_1 = limit - cursor;
                    lab0: do {
                        // loop, line 31
                        for (v_2 = 4; v_2 > 0; v_2--)
                        {
                            // (, line 31
                            // try, line 32
                            v_3 = limit - cursor;
                            lab1: do {
                                // (, line 32
                                if (!(I_p1 > 8))
                                {
                                    cursor = limit - v_3;
                                    break lab1;
                                }
                                // [, line 33
                                ket = cursor;
                                // substring, line 33
                                among_var = find_among_b(a_0, 3);
                                if (among_var == 0)
                                {
                                    cursor = limit - v_3;
                                    break lab1;
                                }
                                // ], line 33
                                bra = cursor;
                                switch(among_var) {
                                    case 0:
                                        cursor = limit - v_3;
                                        break lab1;
                                    case 1:
                                        // (, line 33
                                        // delete, line 33
                                        slice_del();
                                        break;
                                }
                            } while (false);
                            // try, line 35
                            v_4 = limit - cursor;
                            lab2: do {
                                // (, line 35
                                if (!(I_p1 > 7))
                                {
                                    cursor = limit - v_4;
                                    break lab2;
                                }
                                // [, line 36
                                ket = cursor;
                                // substring, line 36
                                among_var = find_among_b(a_1, 2);
                                if (among_var == 0)
                                {
                                    cursor = limit - v_4;
                                    break lab2;
                                }
                                // ], line 36
                                bra = cursor;
                                switch(among_var) {
                                    case 0:
                                        cursor = limit - v_4;
                                        break lab2;
                                    case 1:
                                        // (, line 36
                                        // delete, line 36
                                        slice_del();
                                        break;
                                }
                            } while (false);
                            I_p1 = (getCurrent().length());
                            // try, line 39
                            v_5 = limit - cursor;
                            lab3: do {
                                // (, line 39
                                if (!(I_p1 > 6))
                                {
                                    cursor = limit - v_5;
                                    break lab3;
                                }
                                // [, line 40
                                ket = cursor;
                                // substring, line 40
                                among_var = find_among_b(a_2, 22);
                                if (among_var == 0)
                                {
                                    cursor = limit - v_5;
                                    break lab3;
                                }
                                // ], line 40
                                bra = cursor;
                                switch(among_var) {
                                    case 0:
                                        cursor = limit - v_5;
                                        break lab3;
                                    case 1:
                                        // (, line 43
                                        // delete, line 43
                                        slice_del();
                                        break;
                                }
                            } while (false);
                            I_p1 = (getCurrent().length());
                            // try, line 46
                            v_6 = limit - cursor;
                            lab4: do {
                                // (, line 46
                                if (!(I_p1 > 6))
                                {
                                    cursor = limit - v_6;
                                    break lab4;
                                }
                                // [, line 47
                                ket = cursor;
                                // substring, line 47
                                among_var = find_among_b(a_3, 26);
                                if (among_var == 0)
                                {
                                    cursor = limit - v_6;
                                    break lab4;
                                }
                                // ], line 47
                                bra = cursor;
                                switch(among_var) {
                                    case 0:
                                        cursor = limit - v_6;
                                        break lab4;
                                    case 1:
                                        // (, line 50
                                        // delete, line 50
                                        slice_del();
                                        break;
                                }
                            } while (false);
                            I_p1 = (getCurrent().length());
                            // try, line 53
                            v_7 = limit - cursor;
                            lab5: do {
                                // (, line 53
                                if (!(I_p1 > 5))
                                {
                                    cursor = limit - v_7;
                                    break lab5;
                                }
                                // [, line 54
                                ket = cursor;
                                // substring, line 54
                                among_var = find_among_b(a_4, 8);
                                if (among_var == 0)
                                {
                                    cursor = limit - v_7;
                                    break lab5;
                                }
                                // ], line 54
                                bra = cursor;
                                switch(among_var) {
                                    case 0:
                                        cursor = limit - v_7;
                                        break lab5;
                                    case 1:
                                        // (, line 55
                                        // delete, line 55
                                        slice_del();
                                        break;
                                }
                            } while (false);
                            I_p1 = (getCurrent().length());
                            // try, line 58
                            v_8 = limit - cursor;
                            lab6: do {
                                // (, line 58
                                // (, line 58
                                if (!(I_p1 > 6))
                                {
                                    cursor = limit - v_8;
                                    break lab6;
                                }
                                // (, line 58
                                // [, line 59
                                ket = cursor;
                                if (!(in_grouping_b(g_soglasniki, 98, 232)))
                                {
                                    cursor = limit - v_8;
                                    break lab6;
                                }
                                // ], line 59
                                bra = cursor;
                                // test, line 59
                                v_9 = limit - cursor;
                                if (!(in_grouping_b(g_soglasniki, 98, 232)))
                                {
                                    cursor = limit - v_8;
                                    break lab6;
                                }
                                cursor = limit - v_9;
                                // delete, line 59
                                slice_del();
                            } while (false);
                            I_p1 = (getCurrent().length());
                            // try, line 63
                            v_10 = limit - cursor;
                            lab7: do {
                                // (, line 63
                                if (!(I_p1 > 5))
                                {
                                    cursor = limit - v_10;
                                    break lab7;
                                }
                                // [, line 64
                                ket = cursor;
                                // substring, line 64
                                among_var = find_among_b(a_5, 5);
                                if (among_var == 0)
                                {
                                    cursor = limit - v_10;
                                    break lab7;
                                }
                                // ], line 64
                                bra = cursor;
                                switch(among_var) {
                                    case 0:
                                        cursor = limit - v_10;
                                        break lab7;
                                    case 1:
                                        // (, line 64
                                        // delete, line 64
                                        slice_del();
                                        break;
                                }
                            } while (false);
                        }
                    } while (false);
                    cursor = limit - v_1;
                    cursor = limit_backward;                    return true;
                }

        public boolean equals( Object o ) {
            return o instanceof SlovenianStemmer;
        }

        public int hashCode() {
            return SlovenianStemmer.class.getName().hashCode();
        }



}

