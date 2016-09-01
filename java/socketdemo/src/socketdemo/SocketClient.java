package socketdemo;

import java.net.InetSocketAddress;
import java.net.Socket;
import java.io.BufferedOutputStream;
 
public class SocketClient {
    private String address = "127.0.0.1";
    private int port = 9527;
    //private String address = "172.20.10.2";
    //private int port = 8001;
    public SocketClient() {
 
        Socket client = new Socket();
        InetSocketAddress isa = new InetSocketAddress(this.address, this.port);
        
        java.io.BufferedInputStream in;
        try {
            client.connect(isa, 10000);
            
            
            /*BufferedOutputStream out = new BufferedOutputStream(client.getOutputStream());
            out.write("Send From Client ".getBytes());
            out.flush();
            out.close();
            out = null;*/
            
            in = new java.io.BufferedInputStream(client.getInputStream());
            byte[] b = new byte[1024];
            
            int length;
            
            while(true){
                
                String data = "";
                /*
                while ((length = in.read(b)) > 0)
                {
                    data += new String(b, 0, length);
                }*/
                
                length = in.available();
                
                if( length > 0){
                    in.read(b, 0, length);
                    
                    for(int i=0; i<b.length; i++){
                        data += (char)b[i];
                    }
                    
                    //data = new String(b, "UTF-8");
                    
                    System.out.println("[client]length: " + length);
                    System.out.println("[client]" + data);
                }
                
                
                
                

                
                
                //client.close();
                //client = null;
                
                try{ Thread.sleep(100);}
                catch(Exception e){ System.out.println(e.toString()); }


            }
 
        } catch (java.io.IOException e) {
            System.out.println("Socket link error !");
            System.out.println("IOException :" + e.toString());
        }
    }
 
    public static void main(String args[]) {
        new SocketClient();
    }
}