package com.cgtest.sundaySearch;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

/**
 * @author cg
 * describe: use Sunday algorithm to search files by string
 * time: 2017-09-17
 *
 */
public class SundaySearchFile {
	
	public static void main(String [] args) {
		
		
		System.out.println("通过字符串来查找文件，使用Sunday算法");
		Scanner scanner = new Scanner(System.in);
		while(true){
			System.out.println("请输入文件路径('q to exit') :");
			String strFilePath = scanner.nextLine();
			if(strFilePath.equals("q") || strFilePath.equals("Q")) {
				scanner.close();
				break;
			}else if(!strFilePath.equals("")){
				if(new File((strFilePath)).exists() && true) {
					System.out.println("请输入要查找的字符串 :");
					String strSearch = scanner.nextLine();
					if(strSearch.equals("q") || strSearch.equals("Q")) {
						scanner.close();
						break;
					}else {
						
						long startTime = System.currentTimeMillis();
						
						SundaySelf sundaySelf = new SundaySelf();
							
						Map<String, Object> mapTotalFile = sundaySelf.sundaySearchFileByStr(strFilePath, strSearch);
						double userTime = (System.currentTimeMillis() - startTime);
						sundaySelf.showResult(mapTotalFile);
						System.out.println("查找耗时:" + (userTime)/1000 + "s");
						}
						
					}
				}else {
					System.out.println("文件路径" + strFilePath + "不存在");
					continue;
				}
			}
		
	}
}

class SundaySelf{
	ArrayList<File> listFilesObj = null;
	
	@SuppressWarnings("unchecked")
	public void showResult(Map<String, Object> mapTotalFile) {
		
		ArrayList<Object> listMsg = (ArrayList<Object>) mapTotalFile.get("resultMsg");
		System.out.println("<-----查找结果----->");
		System.out.println("查找路径为:" + mapTotalFile.get("searchPath"));
		System.out.println("查找的字符串为:" + mapTotalFile.get("strSearch"));
		if(listMsg == null || listMsg.size() == 0) {
			System.out.println("已扫描文件个数 :" + mapTotalFile.get("fileNum"));
			System.out.println("已扫描字符个数 :" + mapTotalFile.get("totalCharNum"));
			System.out.println("抱歉 , 未查找到相应文件");
		}else {
			System.out.println("包含该字符串的文件路径及详情如下 :");
			for(int i = 0; i < listMsg.size(); i++) {
				Map<String, Object> mapItem = (Map<String, Object>) listMsg.get(i);
				System.out.println("文件" + (i + 1) + "路径 :" + mapItem.get("filePath"));
				System.out.println("出现该字符串的总数 :" + mapItem.get("totalCount"));
				System.out.println("出现该字符串的行数 :" + mapItem.get("lineNum"));
				System.out.println("行数对应的出现次数 :" + mapItem.get("lineExistCount"));
			}
			System.out.println("总查找文件个数 :" + mapTotalFile.get("fileNum"));
			System.out.println("总查找字符个数 :" + mapTotalFile.get("totalCharNum"));
			System.out.println("<-----查找完成----->");
		}
	}
	
	
	public ArrayList<File> getFiles(String strFilePath) {
		
		if(listFilesObj == null) {
			listFilesObj = new ArrayList<File>();
		}

		File fileObj = new File(strFilePath);
		
		if(fileObj.isDirectory()) {
			File fileNextDir [] = fileObj.listFiles();
			for(File fileItem : fileNextDir) {
				if(fileItem.isDirectory()) {
					getFiles(fileItem.getPath());
				}else {
					listFilesObj.add(fileItem);
				}
			}
		}else {
			listFilesObj.add(fileObj);
		}
		return listFilesObj;
	}
	
	
	public Map<String, Object> sundaySearchFileByStr(String strFilePath, String strSearch) {
		
		
		ArrayList<File> listFilesObj = getFiles(strFilePath);
		
		Map<String, Object> mapTotalFile = new HashMap<String, Object>();
		ArrayList<Object> listMsg = new ArrayList<Object>();
		int fileNum = 0;
		long totalCharNum = 0;
		
		for(File listItem : listFilesObj) {
			Map<String, Object> mapFile = new HashMap<String, Object>();
			ArrayList<Integer> listLineNum = new ArrayList<Integer>();
			ArrayList<Integer> listLineExistCount = new ArrayList<Integer>();
			int lineNum = 1;
			int existCount = 0;
			int totalCount = 0;
			try {
				BufferedReader buffererReader = new BufferedReader(new FileReader(listItem));
				String strLine = null;
				while((strLine = buffererReader.readLine()) != null) {
					existCount = sundaySearchStrByStr(strLine, strSearch);
					if(existCount != 0) {
						listLineNum.add(lineNum);
						listLineExistCount.add(existCount);
					}
					totalCharNum += strLine.length();
					totalCount += existCount;
					
					lineNum++;
				}
				buffererReader.close();
				if(totalCount != 0) {
					mapFile.put("filePath", listItem);
					mapFile.put("totalCount", totalCount);
					mapFile.put("lineNum", listLineNum);
					mapFile.put("lineExistCount", listLineExistCount);
				}
				if( mapFile.size() != 0) {
					listMsg.add(mapFile);
				}
				
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			fileNum++;
		}
		if(listMsg.size() != 0) {
			mapTotalFile.put("resultMsg", listMsg);
		}
		mapTotalFile.put("searchPath", strFilePath);
		mapTotalFile.put("strSearch", strSearch);
		mapTotalFile.put("fileNum", fileNum);
		mapTotalFile.put("totalCharNum", totalCharNum);
		
		return mapTotalFile;
		
		
	}
	
	
	public int sundaySearchStrByStr(String strTotal, String strSearch) {
		
		char charTotal [] = strTotal.toCharArray();
		char charSearch [] = strSearch.toCharArray();
		
		int t = 0;
		int s = 0;
		int existCount = 0;
		while(s < charSearch.length && t < charTotal.length) {
			
			if(charSearch[s] == charTotal[t]) {
				
				if((s + 1) != charSearch.length) {
					s++;
					t++;
				}else {
					existCount++;
					if(charTotal.length - (t + 1) >= charSearch.length) {
						s = 0;
						t++;
					}else {
						break;
					}
				}
			}else {
				int num = t + charSearch.length;
				int index = -1;
				if(num < charTotal.length) {
					
					for(int i = 0; i < charSearch.length; i++) {
						if(charTotal[num] == charSearch[i]) {
							index = i;
							break;
						}
					}
					if(index != -1) {
						t = t + (charSearch.length - index);
						s = 0;
						
					}else {
						t = num + 1;
						s = 0;
					}
				}else {
					break;
				}
			}
			if(t >= charTotal.length) {
				break;
			}
		}
		return existCount;
		
	}
}
