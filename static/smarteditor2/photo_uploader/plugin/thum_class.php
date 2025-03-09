<?
class thumb { 
	public function __construct() {}
	// create thumbnail, will accept jpeg and gif. 
	public static function create_thumbnail($file, $max_side = false, $fixed = false) { 
		// 1 = GIF, 2 = JPEG 
		if(!$max_side) $max_side = 100; 
		if(file_exists($file)) { 
			$type = getimagesize($file); 

			if(!function_exists('imagegif') && $type[2] == 1) { 
				$error = 'Filetype not supported. Thumbnail not created.'; 
			} 
			elseif (!function_exists('imagejpeg') && $type[2] == 2) { 
				$error = 'Filetype not supported. Thumbnail not created.'; 
			} 
			else {	
				// create the initial copy from the original file 
				if($type[2] == 1) { 
					$image = imagecreatefromgif($file); 
				} 
				elseif($type[2] == 2) { 
					$image = imagecreatefromjpeg($file); 
				} 
				elseif($type[2] == 3) { 
					$image = imagecreatefrompng($file); 
					imagealphablending($image, true);
				}

				if(function_exists('imageantialias')) 
				imageantialias($image, TRUE); 

				$image_attr = getimagesize($file); 

				// figure out the longest side 

				if($image_attr[0] > $image_attr[1]): 
					$image_width = $image_attr[0]; 
					$image_height = $image_attr[1]; 
						
					if($fixed) { 
						$image_new_width  = $max_side; 
						$image_new_height = (int)($max_side * 3 / 4); 
						// 4:3 ratio 
					} else { 
						$image_new_width = $max_side; 
	
						$image_ratio = $image_width / $image_new_width; 
						$image_new_height = (int) ($image_height / $image_ratio); 
					} 
					//width > height 
				else: 
					$image_width = $image_attr[0]; 
					$image_height = $image_attr[1]; 
					if($fixed) { 
						$image_new_height = $max_side; 
						$image_new_width  = (int)($max_side * 3 / 4); 
						// 3:4 ratio 
					} else { 
						$image_new_height = $max_side; 

						$image_ratio = $image_height / $image_new_height; 
						$image_new_width = (int) ($image_width / $image_ratio); 
					} 
					//height > width 
				endif; 

				$tSize = explode(",",$max_side);
				if(count($tSize)==2){
					$image_new_width=$tSize[0];
					$image_new_height=$tSize[1];
				}

				$thumbnail = imagecreatetruecolor($image_new_width, $image_new_height); 
				@ imagecopyresampled($thumbnail, $image, 0, 0, 0, 0, $image_new_width, $image_new_height, $image_attr[0], $image_attr[1]); 

				//$thumb = preg_replace('!(\.[^.]+)?$!', '.thumbnail'.'$1', basename($file), 1);  //썸네일 파일명 변경
				$thumb = basename($file); //썸네일 파일명 변경 않함
				$thumbpath = str_replace(basename($file), $thumb, $file); 

				// move the thumbnail to it's final destination 
				if($type[2] == 1) { 
					if (!imagegif($thumbnail, $thumbpath)) { 
						$error = 'Thumbnail path invalid'; 
					} 
				} 
				elseif($type[2] == 2) { 
					if (!imagejpeg($thumbnail, $thumbpath)) { 
						$error = 'Thumbnail path invalid'; 
					} 
				}
				elseif($type[2] == 3) { 
					if (!imagepng($thumbnail, $thumbpath,9)) { 
						$error = 'Thumbnail path invalid'; 
					} 
				}
			} 
		} else { 
			$error = 'File not found'; 
		} 

		if(!empty($error)) { 
			die($error); 
		} else { 
			return $thumbpath; 
		} 

	} 

};

?>