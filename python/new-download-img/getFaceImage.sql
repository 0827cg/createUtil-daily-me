/*
describe: get face_id and pic
author: cg
create time: 2018-06-28
*/

SELECT
	face_id AS faceId,
	IFNULL(pic_url_1, '') AS picUrl_1,
	IFNULL(pic_url_2, '') AS picUrl_2
FROM
	htg_face
WHERE
	effect = 1
AND active = 1