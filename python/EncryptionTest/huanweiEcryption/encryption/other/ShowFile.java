import java.io.File;

public class ShowFile {
	public static void main(String [] args){
		String filePath = "/home/cg/Work/Testnew/Java";
		printFile(new File(filePath), 1);
	}
	public static void printFile(File fileDir,int n){
		if(fileDir.isDirectory()){
			File nextDir [] = fileDir.listFiles();
			for(int i = 0;i < nextDir.length;i++){
				for(int j = 0;j < n;j++){
					System.out.print("| - - -");
				}
				System.out.println(nextDir[i].getName());
				if(nextDir[i].isDirectory()){
					printFile(nextDir[i],n + 1);
				}
			}
		}
	}
}
