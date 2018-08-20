/*
describe: get face_id and pic to download for specific
author: cg
create time: 2018-07-25
*/


SELECT
	face_id AS faceId,
	IFNULL(pic_url_1, '') AS picUrl_1,
	IFNULL(pic_url_2, '') AS picUrl_2
FROM
	htg_face
WHERE
	device_id = '000c4303137e'
AND	effect = 1
AND active = 1