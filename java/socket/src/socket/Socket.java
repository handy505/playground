package socket;

public class Socket {

    public static void main(String args[])
    {
        if(args.length==0)
            System.out.println("input parameter: server or client");
        if(args[0].equals("server"))
            (new SocketServer()).start();
        else
            new SocketClient();
    }
    
}
