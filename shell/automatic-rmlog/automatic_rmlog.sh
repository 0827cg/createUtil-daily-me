#!/bin/bash

#Describe: remove tomcat log file
#Author: cg错过
#Time: 2017-10-31

#----------USER CONFIG----------#

TOMCAT_DIR=/home/xm6f/dev

#unit M
MAX_TOMCAT_SIZE=2048

#unit percentage
MAX_HOME_SIZE=30

RMLOG_PATH=/usr/scripts/automatic/rmlog_log

TODAY=$(date +%y%m%d)
TIME=$(date +%Y-%m-%d-%T)

#-------------------------------#



function writer_log() {
	
	#创建文件和写入文件
	#当参数1为空，则创建文件，否则写入文件
	#当参数2为空，则表示默认句末换行，否则不换行

	if [[ $1 = '' ]]
	then
		echo "" > ${RMLOG_PATH}/rmlog_log-${TODAY}.txt
	else
		if [[ $2 = '' ]]
		then
			echo "$1" >> ${RMLOG_PATH}/rmlog_log-${TODAY}.txt
		else
			echo -e "$1\c" >> ${RMLOG_PATH}/rmlog_log-${TODAY}.txt
		fi
	fi
}

function check_logExist() {

	#检测文件存放日志的路径及文件是否存在
	#如若不存在，则依次创建

	if [[ ! -d "${RMLOG_PATH}" ]]
	then
		mkdir ${RMLOG_PATH}
	fi
	if [[ ! -f "${RMLOG_PATH}/rmlog_log-${TODAY}.txt" ]]
	then
		writer_log
	fi
}

function review_disk() {

	RE_DF_RESULT=$(df -Th)
	writer_log "清理后的系统挂载点容量信息如下:"
	writer_log "${RE_DF_RESULT}"
	cd ${TOMCAT_DIR}
	ALL_TOMCAT=$(du -sh * | grep tomcat)
	writer_log "清理后的所有tomcat分别占用的容量详情如下:"
	writer_log ${ALL_TOMCAT}
}

function doTomcat() {

	#启动tomcat
	#参数1表示tomcat名字
	#参数2的值为'start'或'stop',表示启动或停止

	${TOMCAT_DIR}/${1}/bin/./catalina.sh ${2}
	if [[ $? -eq 0 ]]
	then
		writer_log "**-->脚本已对${1}执行${2}命令"
	else
		writer_log "**-->脚本未成功对${1}执行${2}命令"
	fi

	if [[ ${2} = 'start' ]]
	then
		START_TOM_RESULT=$(ps -ef | grep tomcat)
		if [[ $START_TOM_RESULT =~ "$1" ]]
		then
			writer_log "**-->${1}已成功${2}"
		else
			writer_log "**-->脚本对${1}操作未成功，请手动${2}"
		fi
	fi
}

function rmTomcat_log() {

        #删除tomcat日志
        #参数1为tomcat的名字

        cd ${TOMCAT_DIR}/${1}/logs
        rm -rf *
        if [[ $? -eq 0 ]]
        then
                writer_log "-->脚本已删除${1}的日志,将执行启动"
                doTomcat ${1} "start"
		review_disk
        else
                writer_log "-->脚本为成功删除${1}的日志,请手动删除"
	fi

}

function doTomcat_log() {

        #进行操作tomcat,包括调用删除日志方法
        #参数1表示tomcat的名字
        
        doTomcat ${1} "stop"

	writer_log "进程睡眠3秒..."
	sleep 3

        STOP_TOM_RESULT=$(ps -ef | grep tomcat)
        if [[ $STOP_TOM_RESULT =~ ${1} ]]
        then
                writer_log "**-->脚本对${1}操作未成功，请手动停止"
        else
                writer_log "**-->${1}已成功停止运行,将进行删除日志操作"
                rmTomcat_log ${1}
        fi      

}

function find_maxUse() {

        #在dev目录中查找使用量最大的tomcat

        cd ${TOMCAT_DIR}
        MAX_SIZE=$(du -sm * | grep tomcat | sort -rn | head -n 1 | awk '{print $1}')
        MAX_NAME=$(du -sm * | grep tomcat | sort -rn | head -n 1 | awk '{print $2}')
        ALL_TOMCAT=$(du -sh * | grep tomcat)
        writer_log "所有tomcat分别占用的容量详情如下:"
        writer_log "${ALL_TOMCAT}"

        if [[ ${MAX_SIZE} -gt ${MAX_TOMCAT_SIZE} ]]
        then
                writer_log "容量占用最大的tomcat使用量大于$[ ${MAX_TOMCAT_SIZE} / 1024 ]G,将进行删除日志操作"
                doTomcat_log ${MAX_NAME}
        else
                writer_log "容量占用最大的tomcat使用量小于$[ ${MAX_TOMCAT_SIZE} / 1024 ]G,不进行操作"
		writer_log "可能有其他项目占用了内存"
        fi

}

function check_homeDisk() {

	#检测home挂载点容量及系统所有挂载点容量使用信息

        DF_RESULT=$(df -Th)
        DF_HOME_RESULT=$(df -h | grep /home | awk '{print $5}' | cut -f 1 -d "%")
        echo ${DF_HOME_RESULT}
        writer_log "home挂载点容量已使用: ${DF_HOME_RESULT}%"
        writer_log "系统所有挂载点容量信息如下:"
        writer_log "${DF_RESULT}"

	if [[ ${DF_HOME_RESULT} -ge ${MAX_HOME_SIZE} ]]
	then
		writer_log "home挂载点已超过${MAX_HOME_SIZE}%"
		find_maxUse
	else
		writer_log "home挂载点已用容量未超过${MAX_HOME_SIZE}%,不再显示详情"
	fi

}

function init_rmLog() {

	#脚本主函数
	
	check_logExist
	writer_log "===============${TIME}==============="
	check_homeDisk
	writer_log "==============="	

}

init_rmLog


