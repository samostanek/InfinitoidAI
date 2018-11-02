import java.io.*;

void setup() {
  size(1000, 1000);
  System.out.println("RUNTIME: Processing render subprocess started.");
  try {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    fill(255, 0, 0);
    ellipse(100, 100, 100, 100);
    String s = br.readLine();
    System.out.println("RENDER: ");
    fill(0, 255, 0);
    ellipse(100, 100, 100, 100);
    s = br.readLine();
    System.out.println("RUNTIME: Processing render subprocess terminated.");
  } catch(IOException e) {
    e.printStackTrace();
  }
}
