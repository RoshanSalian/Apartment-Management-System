function setImg(imgName){
	document.getElementById("imgPlace").innerHTML = '<img src="http://vispi.pythonanywhere.com/static/images/'+imgName+'" height="100%" style="text-align: center">'
}

function remImg(){
	document.getElementById("imgPlace").innerHTML = ''
}

function skillsModal(){
	modalHead = document.getElementById("infoModalHead")
	modalBody = document.getElementById("infoModalBody")

	modalHead.innerHTML = '<button type="button" class="close zoom" data-dismiss="modal">&times;</button>'
	modalHead.innerHTML += '<center><div id = "imgPlace" style="width: 250px; height: 50px"></div></center>'
	modalHead.innerHTML += '<center><font class="zoom" style="display: block;"><strong>Skills</strong></font></center>'

	modalHead.innerHTML += '<hr>'
	
	modalBody.innerHTML = '<div class="progress zoom" onmouseover="setImg(&quot;java.jpg&quot;)" onmouseout="remImg()" style="margin-top: -20px; height:25px">' +
							'<div class="progress-bar" style="width:90%">' +
								'<strong>Java</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;android.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar bg-success" style="width:85%">' +
								'<strong>Android App Development</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;python.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar bg-info" style="width:75%">' +
								'<strong>Python</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;html.jpg&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar bg-warning" style="width:70%">' +
								'<strong>HTML</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;css.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar" style="width:70%">' +
								'<strong>CSS</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;js.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar bg-warning" style="width:67%">' +
								'<strong>JavaScript</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;c.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar bg-dark" style="width:60%">' +
								'<strong>C</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;cpp.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar bg-info" style="width:60%">' +
								'<strong>C++</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;sql.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar" style="width:60%">' +
								'<strong>SQL</strong>' +
							'</div>' +
						'</div>'

	modalBody.innerHTML += '<div class="progress zoom" onmouseover="setImg(&quot;latex.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; height:25px">' +
							'<div class="progress-bar bg-dark" style="width:50%">' +
								'<strong>LaTeX</strong>' +
							'</div>' +
						'</div>'
}


function eduModal(){
	modalHead = document.getElementById("infoModalHead")
	modalBody = document.getElementById("infoModalBody")

	modalHead.innerHTML = '<button type="button" class="close zoom" data-dismiss="modal">&times;</button>'
	modalHead.innerHTML += '<center><div id = "imgPlace" style="width: 250px; height: 50px"></div></center>'
	modalHead.innerHTML += '<center><font class="zoom" style="display: block;"><strong>Education</strong></font></center>'

	modalHead.innerHTML += '<hr>'

	modalBody.innerHTML = '<font class="zoomText" onmouseover="setImg(&quot;nitk.png&quot;)" onmouseout="remImg()" style="margin-top: -20px; font-size: 13px"><strong>Pursuing degree for Master of Technology (MTech) (2019 - )</strong></font>'
	modalBody.innerHTML += '<ul class="list-group">'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;nitk.png&quot;)" onmouseout="remImg()" style="background-color: var(--redLight)"><font style="font-size: 13px">Branch: <strong>Computer Science - Information Security</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;nitk.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepGreenLight)"><font style="font-size: 13px">At <strong>National Institute of Technology Karnataka, Surathkal.</strong></font></li>'
	modalBody.innerHTML += '</ul>'

	modalBody.innerHTML += '<font class="zoomText" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="font-size: 13px; margin-top: 10px"><strong>Completed degree for Bachelor of Technology (BTech) (2015 - 2019)</strong></font>'

	modalBody.innerHTML += '<ul class="list-group">'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="background-color: var(--orangeLight)"><font style="font-size: 13px">Branch: <strong>Information Technology</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepBlueLight)"><font style="font-size: 13px">Minor Specialization: <strong>Data Analytics</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepGreenLight)"><font style="font-size: 13px">At <strong>Manipal Institute of Technology, Manipal</strong>.</font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="background-color: var(--redLight)"><font style="font-size: 13px">Chose this course due to <strong>interest in computers</strong> and <strong>love for coding</strong>.</font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepBlueLight)"><font style="font-size: 13px">Electives studied: <strong>Astronomy, Optimization Techniques</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="background-color: var(--orangeLight)"><font style="font-size: 13px">Lived in an amazing environment and really <strong>grew as a person</strong> during the four years spent there.</font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;manipal.png&quot;)" onmouseout="remImg()" style="background-color: var(--redLight)"><font style="font-size: 13px">Completed the course with <strong>9.08 CGPA</strong>.</font></li>'
	modalBody.innerHTML += '</ul>'
	
	modalBody.innerHTML += '<font class="zoomText" onmouseover="setImg(&quot;pace.png&quot;)" onmouseout="remImg()" style="font-size: 13px; margin-top: 10px"><strong>Completed Higher Secondary Education (HSC) (2013 - 2015)</strong></font>'

	modalBody.innerHTML += '<ul class="list-group">'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;pace.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepGreenLight)"><font style="font-size: 13px">Stream: <strong>Science (PCM)</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;pace.png&quot;)" onmouseout="remImg()" style="background-color: var(--orangeLight)"><font style="font-size: 13px">At <strong>Pace Junior Science College, Thane</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;pace.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepBlueLight)"><font style="font-size: 13px">Board Exam Score: <strong>86.46%</strong></font></li>'	
	modalBody.innerHTML += '</ul>'

	modalBody.innerHTML += '<font class="zoomText" onmouseover="setImg(&quot;vvhs.png&quot;)" onmouseout="remImg()" style="font-size: 13px; margin-top: 10px"><strong>Completed Primary and Secondary Education (SSC) (2000 - 2013)</strong></font>'

	modalBody.innerHTML += '<ul class="list-group">'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;vvhs.png&quot;)" onmouseout="remImg()" style="background-color: var(--redLight)"><font style="font-size: 13px">At <strong>Vasant Vihar High School & Junior College, Thane</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;vvhs.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepGreenLight)"><font style="font-size: 13px">Board Exam Score: <strong>87.27%</strong></font></li>'
	modalBody.innerHTML += '</ul>'

}

function projModal(){
	modalHead = document.getElementById("infoModalHead")
	modalBody = document.getElementById("infoModalBody")

	modalHead.innerHTML = '<button type="button" class="close zoom" data-dismiss="modal">&times;</button>'
	modalHead.innerHTML += '<center><div id = "imgPlace" style="width: 250px; height: 50px"></div></center>'
	modalHead.innerHTML += '<center><font class="zoom" style="display: block;"><strong>Projects</strong></font></center>'

	modalHead.innerHTML += '<hr>'

	modalBody.innerHTML = '<font class="zoomText" onmouseover="setImg(&quot;kh.jpg&quot;)" onmouseout="remImg()" style="margin-top: -20px; font-size: 13px"><strong>KH Antibiotic Policy (2017)</strong></font>'
	modalBody.innerHTML += '<ul class="list-group">'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;kh.jpg&quot;)" onmouseout="remImg()" style="background-color: var(--deepGreenLight)"><font style="font-size: 13px">Developed for <strong>Kasturba Hospital, Manipal.</strong></font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;kh.jpg&quot;)" onmouseout="remImg()" style="background-color: var(--redLight)"><font style="font-size: 13px">Succesfully developed, in active use.</font></li>'
	modalBody.innerHTML += '</ul>'

	modalBody.innerHTML += '<font class="zoomText" onmouseover="setImg(&quot;lena.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; font-size: 13px"><strong>Edge Detection By Recursively Dividing Regions Within Image (2019)</strong></font>'
	modalBody.innerHTML += '<ul class="list-group">'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;lena.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepBlueLight)"><font style="font-size: 13px"><strong>Final year project</strong> while pursuing BTech.</font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;lena.png&quot;)" onmouseout="remImg()" style="background-color: var(--orangeLight)"><font style="font-size: 13px">Successfully developed and implemented.</font></li>'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;lena.png&quot;)" onmouseout="remImg()" style="background-color: var(--deepGreenLight)"><font style="font-size: 13px">Publication pending.</font></li>'
	modalBody.innerHTML += '</ul>'

	modalBody.innerHTML += '<font class="zoomText" onmouseover="setImg(&quot;android.png&quot;)" onmouseout="remImg()" style="margin-top: 10px; font-size: 13px"><strong>Miscellaneous projects in Android app development</strong></font>'
	modalBody.innerHTML += '<ul class="list-group">'
	modalBody.innerHTML += '<li class="list-group-item py-1 zoom roundCorner" onmouseover="setImg(&quot;android.png&quot;)" onmouseout="remImg()"" style="background-color: var(--redLight)"><font style="font-size: 13px"><strong>Multiple apps</strong> developed for fun or personal use.</font></li>'
	modalBody.innerHTML += '</ul>'
}

function sendMsg(){

	if (window.confirm("Sorry! Sending messages is not available at this local implementation.\nPlease visit vispi.pythonanywhere.com to access this.\nRedirect to it?")) {
		window.location.href='http://vispi.pythonanywhere.com';
	};
}