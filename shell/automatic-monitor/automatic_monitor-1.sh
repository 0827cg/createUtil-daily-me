#!/bin/bash

#Describe: Monitor Control System.
# tomcat, nginx, redis
#Author: cg
#Time: 2017-08-31

#----------USER CONFIG----------#

COMPUTER_NAME=149
TOMCAT_DIR=/usr/local/tomcat
REDIS_DIR=/home/xm6f/dev/redis
NGINX_DIR=/usr/local/nginx

PORT_1=8080
PORT_2=8081
PORT_3=8082

PORT_1_FILENAME=lotmall-8080
PORT_2_FILENAME=mango-8081
PORT_3_FILENAME=tomcat-8082

#REDIS_PORT=6379

#
GEN_FILE_TYPE=/dev/mapper/cl-root

EMAIL_ADDR_1=1542723438@qq.com
EMAIL_ADDR_2=2843940784@qq.com

#-------------------------------#

TODAY_HMS=$(date +%y%m%d%H%M%S)
TODAY_H=$(date +%y%m%d%H)
YESTERDAY=$(date -d "yesterday" +%y%m%d)
TIME=$(date +%Y-%m-%d-%T)
HOUR=$(date +%H)
MIN=$(date +%M)


function createEmail_content() {
	if [[ $2 = -h ]]
	then
		if [[ $3 -eq 0 ]]
		then
			echo "$1" >> email_content-${TODAY_H}.txt
		else
			echo -e "$1\c" >> email_content-${TODAY_H}.txt
		fi
	else
		if [[ $3 -eq 0 ]]
		then
			echo "$1" >> email_content-${TODAY_HMS}.txt
		else
			echo -e "$1\c" >> email_content-${TODAY_HMS}.txt
		fi
	fi
}

function createEmail_errContent() {
        if [[ $2 = -h ]]
        then
                if [[ $3 -eq 0 ]]
                then
                        echo "$1" >> email_err-${TODAY_H}.txt
                else
                        echo -e "$1\c" >> email_err-${TODAY_H}.txt
                fi
        else
                if [[ $3 -eq 0 ]]
                then
                        echo "$1" >> email_err-${TODAY_HMS}.txt
                else
                        echo -e "$1\c" >> email_err-${TODAY_HMS}.txt
                fi
        fi
}


function startTomcat() {
	${1}/bin/./catalina.sh start
	if [[ $? -eq 0 ]]
	then
		createEmail_content "**-->脚本已对tomcat${2}执行启动命令"
	else
		createEmail_content "**-->脚本未成功对tomcat${2}执行命令"
	fi
	START_TOM_RESULT=$(ps -ef | grep tomcat)
	if [[ $START_TOM_RESULT =~ "$2" ]]
	then
		createEmail_content "**-->tomcat${2}已成功启动"
	else
		createEmail_content "**-->tomcat${2}启动未成功，请手动启动"
	fi	
}

function startRedis() {
	${1}/./redis-server redis.conf
	if [[ $? -eq 0 ]]
	then
		createEmail_content "**-->脚本已对redis执行启动命令"
	else
		createEmail_content "**-->脚本未成功对reids执行命令"
	fi
	START_RED_RESULT=$(ps -ef | grep 6379)
	if [[ $START_RED_RESULT =~ "6379" ]]
	then
		createEmail_content "**-->redis已成功启动"
	else
		createEmail_content "**-->redis启动未成功，请手动启动"
	fi
}
		

function startNginx() {
	${1}/sbin/./nginx
	if [[ $? -eq 0 ]]
	then
		createEmail_content "**-->脚本已对nginx执行启动命令"
	else
		createEmail_content "**-->脚本未成功对nginx执行命令"
	fi
	START_NGINX_RESULT=$(ps -ef | grep nginx)
	if [[ $START_NGINX_RESULT =~ "nginx:" ]]
	then
		createEmail_content "**-->nginx已成功启动"
	else
		createEmail_content "**-->nginx启动未成功，请手动启动"
	fi
}


function createAll_tail() {

createEmail_content "======================================" $1
createEmail_content "---林繁" $1
createEmail_content "---$TIME" $1

}

function automatic_h() {

	echo "" > email_content-${TODAY_H}.txt

	createEmail_content "${COMPUTER_NAME}今日${HOUR}时脚本自动执行结果" -h
	createEmail_content "======================================" -h

	TOMCAT_STATUS=$(ps -ef | grep tomcat)

	if [[ $TOMCAT_STATUS =~ "$PORT_1" ]]
	then
		createEmail_content "* tomcat${PORT_1}---已在运行" -h 1
		TOMCAT_1_LOG=$(tail -n 150 ${TOMCAT_DIR}/${PORT_1_FILENAME}/logs/catalina.out)
		if [[ $TOMCAT_1_LOG =~ "exception" ]]
		then
			createEmail_content "---日志输出异常" -h
			createEmail_errContent "===============${COMPUTER_NAME}-${PORT_1}-输出日志===============" -h
			createEmail_errContent "$TOMCAT_1_LOG" -h
		else
			createEmail_content "---日志输出正常" -h
		fi
	else
		createEmail_content "* tomcat${PORT_1}---未运行" -h

	fi

	if [[ $TOMCAT_STATUS =~ "$PORT_2" ]]
	then
        	createEmail_content "* tomcat${PORT_2}---已在运行" -h 1
        	TOMCAT_2_LOG=$(tail -n 150 ${TOMCAT_DIR}/${PORT_2_FILENAME}/logs/catalina.out)
        	if [[ $TOMCAT_2_LOG =~ "exception" ]]
        	then
                	createEmail_content "---日志输出异常" -h
                	createEmail_errContent "===============${COMPUTER_NAME}-${PORT_2}-输出日志===============" -h
                	createEmail_errContent "$TOMCAT_2_LOG" -h
        	else
                	createEmail_content "---日志输出正常" -h
        	fi
	else
        	createEmail_content "* tomcat${PORT_2}---未运行" -h

	fi

	if [[ $TOMCAT_STATUS =~ "$PORT_3" ]]
	then
        	createEmail_content "* tomcat${PORT_3}---已在运行" -h 1
        	TOMCAT_3_LOG=$(tail -n 150 ${TOMCAT_DIR}/${PORT_3_FILENAME}/logs/catalina.out)
        	if [[ $TOMCAT_3_LOG =~ "exception" ]]
        	then
                	createEmail_content "---日志输出异常" -h
                	createEmail_errContent "===============${COMPUTER_NAME}-${PORT_3}-输出日志===============" -h
                	createEmail_errContent "$TOMCAT_3_LOG" -h
        	else
                	createEmail_content "---日志输出正常" -h
        	fi
	else
        	createEmail_content "* tomcat${PORT_3}---未运行" -h
	fi

	REDIS_STATUS=$(ps -ef | grep 6379)
	if [[ $REDIS_STATUS =~ "redis-server" ]]
	then
		createEmail_content "* redis已在运行" -h
	else
		createEmail_content "* redis未运行" -h
	fi

	NGINX_STATUS=$(ps -ef | grep nginx)
	if [[ $NGINX_STATUS =~ "nginx:" ]]
	then
		createEmail_content "* nginx已在运行" -h
	else
		createEmail_content "* nginx未运行" -h
	fi

	#DISK_GEN_STATUS=$(df -h | grep /dev/m | awk '{print $5}')
	#createEmail_content "根目录使用量为$DISK_GEN_STATUS"

	DISK_GEN_STATUS=$(df -h | grep $GEN_FILE_TYPE | awk '{print $5}' | cut -f 1 -d "%")
	if [[ $DISK_GEN_STATUS -lt 50 ]]
	then
		createEmail_content "* 根目录使用量较小---已使用${DISK_GEN_STATUS}%" -h
	else
		createEmail_content "* 根目录使用量较大---已使用${DISK_GEN_STATUS}%" -h
	fi


	echo -e "\n\n" >> email_content-${TODAY_H}.txt

	createAll_tail -h
}


function automatic_hms() {

	TOMCAT_STATUS=$(ps -ef | grep tomcat)

	if [[ $TOMCAT_STATUS =~ "$PORT_1" ]]
	then
		TOMCAT_1_LOG=$(tail -n 150 ${TOMCAT_DIR}/${PORT_1_FILENAME}/logs/catalina.out)
		TOMCAT_1_DIR=${TOMCAT_DIR}/${PORT_1_FILENAME}
		if [[ $TOMCAT_1_LOG =~ "exception" ]]
		then
			createEmail_content "* tomcat${PORT_1}---已运行---但日志输出异常"
			createEmail_errContent "===============${COMPUTER_NAME}-${PORT_1}-输出日志==============="
			createEmail_errContent "$TOMCAT_1_LOG"
		fi
	else
		createEmail_content "* tomcat${PORT_1}---未运行"
                createEmail_content "**-->脚本将尝试进行启动...."
                if [[ -x "${TOMCAT_DIR}/${PORT_1_FILENAME}" ]]
                then
                        startTomcat ${TOMCAT_DIR}/${PORT_1_FILENAME} ${PORT_1}
                else
                        createEmail_content "**-->tomcat${PORT_1}路径不存在"
                        createEmail_content "**-->脚本启动tomcat${PORT_1}失败"
                fi
	fi

	if [[ $TOMCAT_STATUS =~ "$PORT_2" ]]
	then
        	TOMCAT_2_LOG=$(tail -n 150 ${TOMCAT_DIR}/${PORT_2_FILENAME}/logs/catalina.out)
        	if [[ $TOMCAT_2_LOG =~ "exception" ]]
        	then
                	createEmail_content "tomcat${PORT_2}---已运行---但日志输出异常"
                	createEmail_errContent "===============${COMPUTER_NAME}-${PORT_2}-输出日志==============="
                	createEmail_errContent "$TOMCAT_2_LOG"
        	fi
	else
        	createEmail_content "* tomcat${PORT_2}---未运行"
                createEmail_content "**-->脚本将尝试进行启动...."
                if [[ -x "${TOMCAT_DIR}/${PORT_2_FILENAME}" ]]
                then
                        startTomcat ${TOMCAT_DIR}/${PORT_2_FILENAME} ${PORT_2}
                else
                        createEmail_content "**-->tomcat${PORT_2}路径不存在"
                        createEmail_content "**-->脚本启动tomcat${PORT_2}失败"
                fi
	fi

	if [[ $TOMCAT_STATUS =~ "$PORT_3" ]]
	then
        	TOMCAT_3_LOG=$(tail -n 150 ${TOMCAT_DIR}/${PORT_2_FILENAME}/logs/catalina.out)
        	if [[ $TOMCAT_3_LOG =~ "exception" ]]
        	then
                	createEmail_content "tomcat${PORT_3}---已运行---但日志输出异常"
                	createEmail_errContent "===============${COMPUTER_NAME}-${PORT_3}-输出日志==============="
                	createEmail_errContent "$TOMCAT_3_LOG"
        	fi
	else
        	createEmail_content "* tomcat${PORT_3}---未运行"
                createEmail_content "**-->脚本将尝试进行启动...."
                if [[ -x "${TOMCAT_DIR}/${PORT_3_FILENAME}" ]]
                then
                        startTomcat ${TOMCAT_DIR}/${PORT_3_FILENAME} ${PORT_3}
                else
                        createEmail_content "**-->tomcat${PORT_3}路径不存在"
                        createEmail_content "**-->脚本启动tomcat${PORT_3}失败"
                fi
	fi

	REDIS_STATUS=$(ps -ef | grep 6379)
	if [[ ! $REDIS_STATUS =~ "redis-server" ]]
	then
		createEmail_content "* redis未运行"
                createEmail_content "**-->脚本将尝试进行启动...."
                if [[ -x "$REDIS_DIR" ]]
                then
                        startRedis $REDIS_DIR
                else
                        createEmail_content "**-->redis路径不存在"
                        createEmail_content "**-->脚本启动redis失败"
                fi
	fi

	NGINX_STATUS=$(ps -ef | grep nginx)
	if [[ ! $NGINX_STATUS =~ "nginx:" ]]
	then
		createEmail_content "* nginx未运行"
                createEmail_content "**-->脚本将尝试进行启动...."
                if [[ -x "$NGINX_DIR" ]]
                then
                        startNginx $NGINX_DIR
                else
                        createEmail_content "**-->nginx路径不存在"
                        createEmail_content "**-->脚本启动nginx失败"
                fi
	fi

	#DISK_GEN_STATUS=$(df -h | grep /dev/m | awk '{print $5}')
	#createEmail_content "根目录使用量为$DISK_GEN_STATUS"

	DISK_GEN_STATUS=$(df -h | grep $GEN_FILE_TYPE | awk '{print $5}' | cut -f 1 -d "%")
	if [[ $DISK_GEN_STATUS -gt 50 ]]
	then
		createEmail_content "* 根目录使用量较大---已使用${DISK_GEN_STATUS}%"
	fi
	
	if [[ -e "email_content-${TODAY_HMS}.txt" ]]
	then
		echo -e "\n\n" >> email_content-${TODAY_HMS}.txt
		createAll_tail
	fi
}


#$HOUR_INT=$(echo $HOUR | sed -r 's/\<0+([1-9]+)/\1/g')

if [[ $MIN = 30 ]]
then
	automatic_h
	if [[ -e "email_err-${TODAY_H}.txt" ]]
	then
	      	mail -s "${COMPUTER_NAME}检测结果" -a email_err-${TODAY_H}.txt -c $EMAIL_ADDR_1 $EMAIL_ADDR_2 < email_content-${TODAY_H}.txt
	else
        	mail -s "${COMPUTER_NAME}检测结果" -c $EMAIL_ADDR_1 $EMAIL_ADDR_2 < email_content-${TODAY_H}.txt
	fi
else
	automatic_hms
	if [[ -e "email_content-${TODAY_HMS}.txt" ]]
	then
		if [[ -e "email_err-${TODAY_HMS}.txt" ]]
		then
			mail -s "${COMPUTER_NAME}有服务未运行" -a email_err-${TODAY_HMS}.txt -c $EMAIL_ADDR_1 $EMAIL_ADDR_2 < email_content-${TODAY_HMS}.txt
		else
			mail -s "${COMPUTER_NAME}有服务未运行" -c $EMAIL_ADDR_1 $EMAIL_ADDR_2 < email_content-${TODAY_HMS}.txt
		fi
	fi
fi


