
//////////////////////////////Variable Definitions//////////////////////////////
//In boolean expressions, elevation is true, azimuth is false

//homeless... aka scrubs
int center_angle_ele = 0;
int center_angle_azi = 0;
int unit_step_out = 13; 
boolean elevation = true;
boolean azimuth = false;

//find_rom_limit();
int cw_pin_azi = A0;
int ccw_pin_azi = A1;
int cw_limit_azi = 0;  
int ccw_limit_azi = 0;
int up_pin_ele = A2;
int down_pin_ele = A3;
int up_limit_ele = 0;
int down_limit_ele = 0;

//find_current_angle(); 
int pot_pin_azi = A4;
int current_angle_azi = 0;
int pot_pin_ele = A5;
int current_angle_ele = 0;

//cautious_state_rom();
int cautious_deg_cw_azi = 0;    
int cautious_deg_ccw_azi = 0;   
int cautious_deg_up_ele = 0;    
int cautious_deg_down_ele = 0;  

//restricted_state_rom();
int restricted_deg_cw_azi = 0;    
int restricted_deg_ccw_azi = 0;   
int restricted_deg_up_ele = 0;    
int restricted_deg_down_ele = 0; 

//state_identifier();
int dampening_gain_azi = 0;
int dampening_gain_ele = 0;
int state = 0;

//trigger_buzzer();
int jamming_alarm_pin = A7;

//init_stepper();
int dir_pin_ele = 50;
int pul_pin_ele = 51;
int ccw_pul_pin = 52;
int cw_pul_pin = 53;

//python handler
String in_char_string = "";
String temp_ele_deg = "";
String temp_azi_deg = "";
String temp_fn_to_call = "";
String temp_axis = "";
char incomingByte = ' ';
boolean ele_dir;
boolean azi_dir;
boolean axis;
long ele_deg;
long azi_deg;
long fn_to_call;
long axis_as_long;

//////////////////////////////Sketch Setup//////////////////////////////
void setup() 
{

    Serial.flush();            //dumps the buffer
    Serial.begin(9600);
    delay(50);
    pinMode(unit_step_out, OUTPUT);   
    pinMode(dir_pin_ele, OUTPUT);  
    pinMode(pul_pin_ele, OUTPUT);      
    pinMode(ccw_pul_pin, OUTPUT); 
    pinMode(cw_pul_pin, OUTPUT);    
    digitalWrite(dir_pin_ele, LOW);
    digitalWrite(pul_pin_ele, LOW); 
    digitalWrite(ccw_pul_pin, LOW);
    digitalWrite(cw_pul_pin, LOW);
    digitalWrite(unit_step_out, LOW); 
 
}

void loop() 
{

    in_char_string = "";
    while(Serial.available() > 0)        // something came across serial
    {
        incomingByte = Serial.read();
        in_char_string += incomingByte; 
    }
    
    //////////////////////////////Python Handler//////////////////////////////
    /*Message Protocol "99, Ele dir, Ele deg, Azi dir, Azi deg, function, axis, 99" 
     *Message Struct   "99,    X   ,    XX  ,    X   ,   XX   ,    X    ,  X  , 99"
     * 0 -> ccw/down
     * 1 -> cw/up
     * 0 -> False = Azimuth
     * 1 -> True = Elevation
     * Degrees being 0-90
     * 
     * test message
     * 991661330099
     * 
     * 222 is the termination message from each fn
     */
        
    delay(50);
    String seat1 = String(in_char_string.charAt(0));
    String seat2 = String(in_char_string.charAt(1));
    if( seat1 == "9" && seat2 == "9")
    {

     //   Serial.flush();
        Serial.print(in_char_string); //sends back the message received.
        
        delayMicroseconds(100);
        temp_azi_deg = in_char_string;
        temp_ele_deg = in_char_string; 
        temp_fn_to_call = in_char_string;  
        temp_axis = in_char_string;      
    
        //Converts the azimuth degrees sent in message to an integer
        temp_azi_deg.remove(0,6);
        temp_azi_deg.remove(2);
        azi_deg = temp_azi_deg.toInt();
    
        //Converts the elevation degrees sent in message to an integer
        temp_ele_deg.remove(5,7);
        temp_ele_deg.remove(0,3);
        ele_deg = temp_ele_deg.toInt();
    
        //Finds the function that shuold be called in the message
        temp_fn_to_call.remove(0,8);
        temp_fn_to_call.remove(1);
        fn_to_call = temp_fn_to_call.toInt();
    
        //Finds the axis that shuold be acuated
        temp_axis.remove(0,9);
        temp_axis.remove(1);
        axis_as_long = temp_axis.toInt();
        
        //Finds the Elevation direction sent in the message
        if (in_char_string.charAt(2) == '0')                     //elevation down
        {
        ele_dir = false;     
        }
        else if (in_char_string.charAt(2) == '1')                //elevation up
        {
        ele_dir = true;
        }
       
        //Finds the Azimuth direction sent in the message
        if (in_char_string.charAt(5) == '0')                     //azimuth ccw
        {
        azi_dir = false;     
        }
        else if (in_char_string.charAt(5) == '1')                //azimuth cw
        {
        azi_dir = true;
        }
    
        if (in_char_string.charAt(9) == '0')                     //This denotes the Azimuth axis
        {
        axis = false;     
        }
        else if (in_char_string.charAt(9) == '1')                //This denotes the elevation axis
        {
        axis = true;
        }
        
        if (fn_to_call == 0)                          //This is to call function zero, it will be used in the initialization of the system.
        {
            find_rom_limit(axis);
        } 
        else if (fn_to_call == 1)                     //This is to call function one, which is the driver stepper one.
        {
            if (axis == true)    
            {
                drive_stepper(ele_dir, ele_deg, axis);
            } 
            else if (axis == false)
            {
                drive_stepper(azi_dir, azi_deg, axis);
            } 
        }
        else if (fn_to_call == 2)                   //This is to call function two, which will trigger the jammeing buzzer
        {
          trigger_buzzer();
        }
    }  
}

void find_rom_limit(boolean axis) 
{
    if (axis == false)                //azimuth
    {
        delay(100); 
        Serial.println("Swinging Clockwise");
        init_stepper(true,axis);
        delay(100); 
        Serial.println("Swinging Counter-Clockwise");
        init_stepper(false,axis);
        delay(100); 
        center_antenna(axis); 

    }
    if (axis == true)           //elevation
    {
        
//        Serial.println("Swinging Up");
        init_stepper(true,axis);
        delay(100); 
//        Serial.println("Swinging Down");
        init_stepper(false,axis);
        delay(100);
        center_antenna(axis); 

    }
}

int find_current_angle(boolean axis)    //Finds the resistence of the pot (through VDR) with a resolution 
{                                       //of 10 bits then converts it to degrees.
  
    analogReference(DEFAULT);
    if (axis == true)                //elevation
    { 
       
        int val = analogRead(pot_pin_ele);
        current_angle_ele = map(val, 0, 1023, 0, 220);              //Maps the 10 bit resolution, 0-1023 to 1-180 degrees
        return current_angle_ele;
   
    }
    else if (axis == false)           //azimuth
    {
       
        int val = analogRead(pot_pin_azi);
        current_angle_azi = map(val, 0, 1023, 0, 220);              //Maps the 10 bit resolution, 0-1023 to 1-180 degrees
        return current_angle_azi;                                   //it looks that out pot has a Rom from 0 to 225 degrees. i need to aust this and fix it
    
    }
}

void init_stepper(boolean dir, boolean axis)  //true meaning elevation           
{                                             //true meaning cw or up 

    if (dir == true && axis == true)                //elevation, up 
    { 
        digitalWrite(dir_pin_ele, HIGH);
        delay(100); 
        do 
        {
            digitalWrite(pul_pin_ele, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(pul_pin_ele, LOW);
            delayMicroseconds(500);            //in microseconds  
            up_limit_ele = find_current_angle(axis); 

        } while (analogRead(up_pin_ele) < 500);
        
    delayMicroseconds(10);
    }  
    else if (dir == false && axis == true)           //elevation, down
    {
        digitalWrite(dir_pin_ele, LOW);
        delay(100); 
        do 
        { 
            digitalWrite(pul_pin_ele, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(pul_pin_ele, LOW);
            delayMicroseconds(500);            //in microseconds   
            down_limit_ele = find_current_angle(axis); 

        } while (analogRead(down_pin_ele) < 500); 
        
    delayMicroseconds(10);
    }
    else if (dir == true && axis == false)          //azimuth, cw
    { 
        delay(100);
        do 
        {
            digitalWrite(cw_pul_pin, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(cw_pul_pin, LOW);
            delayMicroseconds(500);            //in microseconds   
            cw_limit_azi = find_current_angle(axis); 

        } while (analogRead(cw_pin_azi) < 500);

        delay(100);
    }
    else if (dir == false && axis == false)          //azimuth, ccw
    {
        delay(100);
        do
        { 
            digitalWrite(ccw_pul_pin, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(ccw_pul_pin, LOW);
            delayMicroseconds(500);            //in microseconds  
            ccw_limit_azi = find_current_angle(axis); 
        
        } while (analogRead(ccw_pin_azi) < 500); 

        delay(100);
    }
}

void drive_stepper(boolean dir, int deg, boolean axis)    //true meaning elevation           
{                                                         //true meaning cw or up 
                                                          //dampening gain meaning the speed of the motor based on the states
                                                          //1 meaining operational, 2 meaning damped, 3 meaning restricted.
    state_identifier(axis);
    if (dir == true && axis == true)                //elevation, up 
    { 
        digitalWrite(dir_pin_ele, HIGH);
        delayMicroseconds(5);
        for (int i = 0; i <= (deg*1000000); i++)
        {
            state_identifier(axis); 
            if (dampening_gain_ele == 3)
            {
                center_antenna(axis); 
                break;                            
            }
            else if(dampening_gain_ele == 2)
            {
                digitalWrite(pul_pin_ele, HIGH);
                delayMicroseconds(500);            //in microseconds
                digitalWrite(pul_pin_ele, LOW);
                delayMicroseconds(500);             
            }
            else if(dampening_gain_ele == 1)
            {
                digitalWrite(pul_pin_ele, HIGH);
                delayMicroseconds(35);            //in microseconds
                digitalWrite(pul_pin_ele, LOW);
                delayMicroseconds(35);            //in microseconds  
            }          
        }           
    }               
    else if (dir == false && axis == true)           //elevation, down
    { 
        digitalWrite(dir_pin_ele, LOW);
        delayMicroseconds(5);
        for (int i = 0; i <= (deg*1000000); i++)
        {
            state_identifier(axis);
            if (dampening_gain_ele == 3)
            {
                center_antenna(axis); 
                break;                           
            }
            else if(dampening_gain_ele == 2)
            {
                digitalWrite(pul_pin_ele, HIGH);
                delayMicroseconds(500);            //in microseconds
                digitalWrite(pul_pin_ele, LOW);
                delayMicroseconds(500);             
            }
            else if(dampening_gain_ele == 1)
            {
                digitalWrite(pul_pin_ele, HIGH);
                delayMicroseconds(35);            //in microseconds
                digitalWrite(pul_pin_ele, LOW);
                delayMicroseconds(35);            //in microseconds  
            }          
        } 
    }
    else if (dir == true && axis == false)          //azimuth, cw
    { 
        for (int i = 0; i <= (deg*1000000); i++)
        {
            state_identifier(axis);
            if (dampening_gain_azi == 3)
            {
                center_antenna(axis); 
                break;     
            }
            else if(dampening_gain_azi == 2)
            {
                digitalWrite(cw_pul_pin, HIGH);
                delayMicroseconds(500);            //in microseconds
                digitalWrite(cw_pul_pin, LOW);
                delayMicroseconds(500);            
            }
            else if(dampening_gain_azi == 1)
            {
                digitalWrite(cw_pul_pin, HIGH);
                delayMicroseconds(35);            //in microseconds
                digitalWrite(cw_pul_pin, LOW);
                delayMicroseconds(35);  
            }          
        } 
    }
    else if (dir == false && axis == false)          //azimuth, ccw
    { 
        for (int i = 0; i <= (deg*1000000); i++)
        {
            state_identifier(axis);
            if (dampening_gain_azi == 3)
            {
                center_antenna(axis); 
                break;    
            }
            else if(dampening_gain_azi == 2)
            {
                digitalWrite(ccw_pul_pin, HIGH);
                delayMicroseconds(500);            //in microseconds
                digitalWrite(ccw_pul_pin, LOW);
                delayMicroseconds(500);             
            }
            else if(dampening_gain_azi == 1)
            {
                digitalWrite(ccw_pul_pin, HIGH);
                delayMicroseconds(35);            //in microseconds
                digitalWrite(ccw_pul_pin, LOW);
                delayMicroseconds(35);            //in microseconds  
            }          
        } 
    }
}


void trigger_buzzer()
{
   
    pinMode(jamming_alarm_pin, OUTPUT);      
    digitalWrite(jamming_alarm_pin, HIGH);   //used to flip a relay

}


void center_antenna(boolean axis)
{
    if(axis == true)                //elevation
    {
        center_angle_ele = calc_cent_angle(down_limit_ele,up_limit_ele);
        if(current_angle_azi < center_angle_azi)                //moves up
        {
            digitalWrite(dir_pin_ele, HIGH);
            delayMicroseconds(5); 
            do 
            {
            digitalWrite(pul_pin_ele, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(pul_pin_ele, LOW);
            delayMicroseconds(500);            //in microseconds  
            current_angle_ele = find_current_angle(axis);  
            } while (current_angle_azi < center_angle_azi);
        }
        else if(current_angle_ele < center_angle_ele)              //moves down
        {
            digitalWrite(dir_pin_ele, LOW);
            delayMicroseconds(5); 
            do 
            {
            digitalWrite(pul_pin_ele, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(pul_pin_ele, LOW);
            delayMicroseconds(500);            //in microseconds  
            current_angle_ele = find_current_angle(axis);
            } while (current_angle_ele < center_angle_ele);
        }     
    }
    else if(axis == false)           //azimuth
    {
        center_angle_azi = calc_cent_angle(ccw_limit_azi,cw_limit_azi);
        if(current_angle_azi > center_angle_azi)                    //moves cw
        {
            do 
            {
            digitalWrite(cw_pul_pin, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(cw_pul_pin, LOW);
            delayMicroseconds(500);            //in microseconds   
            current_angle_azi = find_current_angle(axis); 

            } while(current_angle_azi > center_angle_azi);
        }
        else if(current_angle_azi < center_angle_azi)                //moves ccw
        {
            do 
            {
            digitalWrite(ccw_pul_pin, HIGH);
            delayMicroseconds(500);            //in microseconds
            digitalWrite(ccw_pul_pin, LOW);
            delayMicroseconds(500);            //in microseconds   
            current_angle_azi = find_current_angle(axis); 

            } while(current_angle_azi < center_angle_azi);
        }     
    }
}



//////////////////////////////Calculation functions//////////////////////////////

void state_identifier(boolean axis)
{
    if (axis == false)          //azimuth
    {
        current_angle_azi = find_current_angle(axis);
        center_angle_azi = calc_cent_angle(ccw_limit_azi,cw_limit_azi);
        cautious_state_rom(axis, ccw_limit_azi, cw_limit_azi);
        restricted_state_rom(axis, ccw_limit_azi, cw_limit_azi);
        
        if(current_angle_azi <= (cautious_deg_ccw_azi-2) && current_angle_azi >= (cautious_deg_cw_azi+2))
        {
            dampening_gain_azi = 1;
        }
        else if(current_angle_azi <= (restricted_deg_ccw_azi-1) && current_angle_azi >= (cautious_deg_ccw_azi+2))
        {
            dampening_gain_azi = 2;
        }
        else if(current_angle_azi >= (restricted_deg_cw_azi+1) && current_angle_azi <= (cautious_deg_cw_azi-2))
        {
            dampening_gain_azi = 2;
        }
        else if(current_angle_azi >= (restricted_deg_ccw_azi+1))
        {
            dampening_gain_azi = 3;
        }
        else if(current_angle_azi <= (restricted_deg_cw_azi-1))
        {
            dampening_gain_azi = 3;
        }
        else
        {
          
        } 
    }   
    else if (axis == true)           //elevation
    {
        find_current_angle(axis);
        center_angle_ele = calc_cent_angle(down_limit_ele,up_limit_ele);
        cautious_state_rom(axis, down_limit_ele, up_limit_ele);
        restricted_state_rom(axis, down_limit_ele, up_limit_ele);

        if(current_angle_ele <= (cautious_deg_down_ele-2) && current_angle_ele >= (cautious_deg_up_ele+2))
        {
            dampening_gain_ele = 1;
        }
        else if(current_angle_ele <= (restricted_deg_down_ele-1) && current_angle_ele >= (cautious_deg_down_ele+2))
        {
            dampening_gain_ele = 2;
        }
        else if(current_angle_ele >= (restricted_deg_up_ele+1) && current_angle_ele <= (cautious_deg_up_ele-2))
        {
            dampening_gain_ele = 2;
        }
        else if(current_angle_ele >= (restricted_deg_down_ele+1))
        {
            dampening_gain_ele = 3;
        }
        else if(current_angle_ele <= (restricted_deg_up_ele-1))
        {
            dampening_gain_ele = 3;
        }
        else
        {
                    
        }
    } 
}

int calc_cent_angle(int uno, int dos)           //larger will be ccw limit on azi and upper in ele
{                                               //done this way because it saves me a fn.
    int center = ((uno/2) + (dos/2));
    return center;
}

void cautious_state_rom(boolean axis, int cw_limit, int ccw_limit)
{

    int center_angle = ((ccw_limit + cw_limit)/2);
    if (axis == true)                //elevation
    {
        cautious_deg_up_ele = (ccw_limit - ((ccw_limit - center_angle) * .2));
        cautious_deg_down_ele = (cw_limit + ((center_angle - cw_limit) * .2));
    }
    else if (axis == false)           //azimuth
    {
        cautious_deg_cw_azi = (ccw_limit - ((ccw_limit- center_angle) * .2));
        cautious_deg_ccw_azi = (cw_limit + ((center_angle - cw_limit) * .2));
    }
}

void restricted_state_rom(boolean axis, int cw_limit, int ccw_limit)
{

    int center_angle = ((ccw_limit + cw_limit)/2);
    if (axis == true)                //elevation
    {
        restricted_deg_up_ele = (ccw_limit - ((ccw_limit- center_angle) * .05));
        restricted_deg_down_ele = (cw_limit + ((center_angle - cw_limit) * .05));
    }
    else if (axis == false)           //azimuth
    {
        restricted_deg_cw_azi = (ccw_limit - ((ccw_limit- center_angle) * .05));
        restricted_deg_ccw_azi = (cw_limit + ((center_angle - cw_limit) * .05));
    }
}

  
