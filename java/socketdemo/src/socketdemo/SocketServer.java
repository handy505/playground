package socketdemo;

import java.io.BufferedOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.Date;
 
public class SocketServer extends java.lang.Thread {
 
    private boolean OutServer = false;
    private ServerSocket server;
    private final int ServerPort = 9527;
 
    public SocketServer() {
        try {
            server = new ServerSocket(ServerPort);
 
        } catch (java.io.IOException e) {
            System.out.println("Socket link error !");
            System.out.println("IOException :" + e.toString());
        }
    }
 
    public void run() {
        Socket socket;
        java.io.BufferedInputStream in;
        
        System.out.println("server start !");
        while (!OutServer) {
            socket = null;
            try {
                synchronized (server) {
                    socket = server.accept();
                }
                System.out.println("get connect: InetAddress = " + socket.getInetAddress());
                // TimeOut
                socket.setSoTimeout(15000);
                
                
                in = new java.io.BufferedInputStream(socket.getInputStream());
                byte[] b = new byte[1024];
                int length;
                
                /*
                in = new java.io.BufferedInputStream(socket.getInputStream());
                byte[] b = new byte[1024];
                String data = "";
                int length;
                while ((length = in.read(b)) > 0)
                {
                    data += new String(b, 0, length);
                }
                System.out.println("server get: " + data);
                in.close();
                in = null;*/
                
                BufferedOutputStream out = new BufferedOutputStream(socket.getOutputStream());
                long last = System.currentTimeMillis();
                while(true){
                    
                    if(System.currentTimeMillis() - last > 1000){
                        last = System.currentTimeMillis();
                        
                        String ts = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(new Date());
                        System.out.println("[server send] " + ts);
                        out.write(ts.getBytes());
                        out.flush();
                        //out.close();
                        //out = null;
                        
                    }
                    
                        

                    
                    
                    String data = "";
                    length = in.available();
                    if( length > 0){
                        in.read(b, 0, length);

                        System.out.print("[server rcv] ");
                        for(int i=0; i<length; i++){
                            data += (char)b[i];
                            System.out.print(Integer.toHexString(b[i]&0xff ));
                        }
                        System.out.print(" (" + data + ")\n");
                        

                        //data = new String(b, "UTF-8");

                        //System.out.println("[client]length: " + length);
                        //System.out.println("[client]" + data);
                    }
                    
                    
                    
                    
                    
                    
                    
                    
                    /*
                    try{ Thread.sleep(1000);}
                    catch(Exception e){ System.out.println(e.toString()); }*/
                }
                
                
                
                //socket.close();
                
 
            } catch (java.io.IOException e) {
                System.out.println("Socket connection error !");
                System.out.println("IOException :" + e.toString());
            }
 
        }
    }
 
    public static void main(String args[]) {
        (new SocketServer()).start();
    }
 
}