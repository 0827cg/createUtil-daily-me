package com.cgtest.kmpsearch;

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
 *	time: 2017-09-15
 *	describe: use kmp algorithm to search files by string
 */
public class KMPsearchFile {
	
	public static void main(String [] args) {
		
		System.out.println("通过字符串来查找文件，使用全匹配的基于部分匹配表的KMP算法");
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
						
						KMPself kmpself = new KMPself();
						int [] kmpTable = kmpself.getKMPtable(strSearch);
							
						Map<String, Object> mapTotalFile = kmpself.kmpSearchFileByStr(strFilePath, strSearch, kmpTable);
						double userTime = (System.currentTimeMillis() - startTime);
						kmpself.showResult(mapTotalFile);
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


class KMPself{
	
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
	
	
	public Map<String, Object> kmpSearchFileByStr(String strFilePath, String strSearch, int kmpTable []) {
		
		/*
		 * 使用kmp算法
		 * 通过字符串搜索文件，将搜索到的结果封装到map，list混合集合中，并最终返回一个map集合
		 */
		
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
					existCount = kmpSearchStrByStr(strLine, strSearch, kmpTable);
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
	
	
	public int kmpSearchStrByStr(String totalStr, String strSearch, int kmpTable []) {
		/*
		 * 参数1为内容字符串
		 * 参数2为输入的搜索字符串即搜索串
		 * 参数3为输入的搜索字符串的部分匹配数值表，为int类型的一维数组
		 * 全匹配的基于部分匹配表的KMP算法
		 * 并不是基于next数组
		 * 
		 * 其返回值是当前字符串中有出现搜索串的个数
		 * 此时并无下标
		 * 
		 */
		char searchChar [] = strSearch.toCharArray();
		char totalChar [] = totalStr.toCharArray();
		
		int s = 0;
		int t = 0;
		//int index = -1;
		int existCount = 0;
		while(s < searchChar.length && t < totalChar.length) {
			if(searchChar[s] == totalChar[t]) {
				if((s + 1) != searchChar.length) {
					s++;
					t++;
				}else {
					existCount++;
					if((totalChar.length - (t + 1)) >= searchChar.length) {
						s = 0;
						t++;
					}else {
						break;
					}
				}
			}else if(s == 0){
				s = 0;
				t++;
			}else {
				s = s - (s - kmpTable[(s - 1)]);
			}
			if((t + 1) >= totalChar.length) {
				break;
			}
		}
		return existCount;
		
	}
	
	
	
	public int[] getKMPtable(String strInput) {
		
		/*
		 * 获取kmp的部分匹配数值表
		 * 但得先获取字符串所有可能长度的最大公告元素长度，将其存放到int数组中返回
		 */
		
		int intTablesLength = strInput.length();
		int kmp_table [] = new int [intTablesLength];
		
		for(int i = 0; i < strInput.length(); i++) {
			String strItem = strInput.substring(0, i + 1);
			int intMaxPublicNum = getMaxPublicNum(strItem);
			kmp_table [i] = intMaxPublicNum;
		}
		return kmp_table;
		
	}
	
	
	public int getMaxPublicNum(String strItem) {
		
		//获取前缀和后缀，并最终对比得到最大的公共元素长度,并返回
		
		int intMaxPublicNum = 0;
		int intItemLength = strItem.length();
		
		String strFront [] = new String [intItemLength - 1];
		String strBack [] = new String [intItemLength - 1];
		
		for(int i = 0; i < intItemLength - 1; i++) {
			strFront[i] = strItem.substring(0, i + 1);
		}
		for(int i = intItemLength; i > 1; i--) {
			strBack[intItemLength - i] = strItem.substring(i - 1, intItemLength);
		}
		
		int n = -1;
		for(int i = 0; i < intItemLength - 1; i++) {
			if(strFront[i].equals(strBack[i])) {
				n = i;
			}
		}
		if(n != -1) {
			intMaxPublicNum = strFront[n].length();
		}
		return intMaxPublicNum;
	}
	
	
}

