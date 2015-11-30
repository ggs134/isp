var myapp = angular.module("myapp", ["ui.bootstrap", "ngResource"]);

function ResourceSetter($resource){
	this.serverUrl = $resource("http://centurio.iptime.org:444/retrieve_data/test_data");
}

myapp.controller("hello", ['$scope', function($scope){
	$scope.helloData = "hello data";
}]);

/*myapp.directive("testAngBoot"), function(){
	return {
		templateUrl:
	}
}*/

myapp.directive("navbar", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/navbar.html",
		scope:{
			
		},
		controller: ['$scope', function($scope){
			$scope.queryToServer = function(){
				jQuery.ajax({
					url: "/retrieve_data/test_data",
					method:"get",
					data: $scope.inputData
				})
				.done(function(data){
					alert(data.hello);
				})
			}
		}]
	}
});

myapp.directive("juitable", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/jui_table.html",
		link: function($scope){
			$scope.resultData = [{ name: "Hong", age: "20", location: "Ilsan" },
			            { name: "Jung", age: "30", location: "Seoul" },
			            { name: "Park", age: "15", location: "Yeosu" },
			            { name: "Kang", age: "32", location: "Seoul" },
			            { name: "Song", age: "12", location: "Gwangju" },
			            { name: "Yoon", age: "22", location: "Damyang" },
			            { name: "Kim", age: "33", location: "Busan" },
			            { name: "Hwang", age: "21", location: "Seoul" }];
			jui.ready([ "uix.table" ], function(table) {
    			table_1 = table("#table", {
			        data: $scope.resultData
    			});
			});
		}
	}
});

myapp.directive("orgmngInputForm", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/orgmng_input_form.html",
		link: function(element){
			jQuery(".btn").css({
				margin: "0px 8px 0px 0px"
			});
			jQuery(".input-form").css({
				margin: "10px 0px"
			});
		},
		controller: ['$scope', function($scope, $element){
			$scope.queryData = function(){
				jQuery('.juitable').css({
					display:"none"
				});
				jQuery('document').ajaxStart(function(){
						jQuery('.progress').css({
							display:"inherit"
						});
				});
				jQuery.ajax({
					method: "get",
					url: "/retrieve_data/test_data",
					data: $scope.orgCode
				})
				.done(function(data){
						jQuery('.progress').css({
							display:"none"
						});
					jQuery('.juitable').slideDown('slow');
				});
			}
		}]
	}
});

myapp.service("resSet", ResourceSetter)
.directive("objmngInputForm", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/objmng_input_form.html",
		link: function(){
			jQuery(".btn").css({
				margin: "0px 8px 0px 0px"
			});
			jQuery(".input-form").css({
				margin: "10px 0px"
			});
		},
		controller: ['$scope','resSet', function($scope, resSet){
			$scope.queryData = function(){
				var result = resSet.serverUrl.get({hello:"hello"}, function(result){
					alert(result.hello);
				});
			}
		}]
	}
});

myapp.directive("orgobjmngInputForm", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/orgobjmng_input_form.html",
		link: function(){
			jQuery(".btn").css({
				margin: "0px 8px 0px 0px"
			});
			jQuery(".input-form").css({
				margin: "10px 0px"
			});
		}
	}
});

myapp.directive("navpills",function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/nav_pills.html",
		controller: ["$scope", function($scope){
			$scope.changeForm = function(num){
				for(var i=1; i < 4; i++){
					jQuery(".tab-elem" + i).css({
						display: "none"
					});
					jQuery(".tab"+i).removeClass("active");
				}
				jQuery(".tab-elem" + num).css({
						display: "inherit"
					});
				jQuery(".tab"+num).addClass("active");
			}
		}]
	}
});

myapp.directive("progressBar", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/progress_bar.html",
		link: function(scope, element, attrs){
			jQuery(element).css({
				paddingLeft: "200px",
				paddingRight:"200px",
				display:"none"
			});
		}
	}
});
