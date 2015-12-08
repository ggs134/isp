var myapp = angular.module("myapp", ["ui.bootstrap", "ngResource", "ui.checkbox"]);

function ResourceSetter($resource){
	this.ServerUrl = $resource("http://ggs134.gonetis.com:444/:querytype/:dept_code/:dept_desc");
}

function ObjectiveResourceSetter($resource){
	this.ServerUrl = $resource("http://ggs134.gonetis.com:444/:querytype/:obj_code/:obj_desc/:obj_priority");
}

function OranizationObjectiveResourceSetter($resource){
	this.ServerUrl = $resource("http://ggs134.gonetis.com:444/:querytype/:dept_code/:obj_code/:dept_obj_resp/:dept_obj_auth/:dept_obj_exp/:dept_obj_work/:dept_obj_ref");
}

myapp.controller("hello", ['$scope', function($scope){
	$scope.helloData = "hello data";
}]);

myapp.directive("navbar", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/navbar.html",
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
			jQuery(".juitable").css({
				display: 'none'
			})
		},
		controller: ['$scope', function($scope){
				jui.ready([ "uix.table" ], function(table) {
	    			$scope.table_1 = table("#table", {scroll: true});
	    			$scope.table_submit = function(datas){
	    				$scope.datas = datas;
	    				$scope.table_1.update($scope.datas.results);
	    				jQuery('.juitable').slideDown('slow');
	    			}
				});
		}]
	}
});

myapp.directive("juiobjtable", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/jui_obj_table.html",
		link: function($scope){
			jQuery(".juiobjtable").css({
				display: 'none'
			})
		},
		controller: ['$scope', function($scope){
				jui.ready([ "uix.table" ], function(table) {
	    			$scope.table_2 = table("#table2", {scroll:true});
	    			$scope.table_obj_submit = function(datas){
	    				$scope.datas = datas;
	    				$scope.table_2.update($scope.datas.results);
	    				jQuery('.juiobjtable').slideDown('slow');
	    			}
				});
		}]
	}
});

myapp.directive("juiorgobjtable", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/jui_orgobj_table.html",
		link: function($scope){
			jQuery(".juiorgobjtable").css({
				display: 'none'
			})
		},
		controller: ['$scope', function($scope){
				jui.ready([ "uix.table" ], function(table) {
	    			$scope.table_3 = table("#table3",{scroll:true});
	    			$scope.table_orgobj_submit = function(datas){
	    				$scope.datas = datas;
	    				$scope.table_3.update($scope.datas.results);
	    				jQuery('.juiorgobjtable').slideDown('slow');
	    			}
				});
		}]
	}
});


myapp.service("resSet", ResourceSetter)
.directive("orgmngInputForm", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/orgmng_input_form.html",
		scope: {
				submit:'&submit'
		},
		link: function(element){
			jQuery(".btn").css({
				margin: "0px 8px 0px 0px"
			});
			jQuery(".input-form").css({
				margin: "10px 0px"
			});
		},
		controller: ['$scope','resSet', function($scope, resSet){
			$scope.querytype = "department";
			$scope.dept_code ='';
			$scope.dept_desc = ''
			$scope.queryOrgData = function(){
				jQuery('.juitable').css({
					display:"none"
				});
			resSet.ServerUrl.get({querytype: $scope.querytype, dept_code: null, dept_desc: null},
					function(results, responseHeader){
							if($scope.dept_code == '' && $scope.dept_desc == '')
								$scope.submit({datas:results});
							else{
								var arrays = [];
								var element;
								while(results.results.length != 0){
									element  = results.results.pop();
									if(element.dept_code == $scope.dept_code && element.dept_desc == $scope.dept_desc)
										arrays.push(element);
									else if($scope.dept_code == '' && element.dept_desc == $scope.dept_desc)
										arrays.push(element);
									else if($scope.dept_desc== '' && element.dept_code == $scope.dept_code)
										arrays.push(element);
								}
								dataObj = {results: arrays}
								$scope.submit({datas:dataObj});
								$scope.dept_code = '';
								$scope.dept_desc = '';
							}
						}
					);
			}
			$scope.saveOrgData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype, dept_code: null, dept_desc: null},
						{a: 'CreateDepartment', dept_code:$scope.dept_code, dept_desc:$scope.dept_desc},
						function(result){
							if(result.results == 1)
								$scope.queryOrgData();	
						});
			}
			$scope.updateOrgData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype, dept_code: null, dept_desc: null},
						{a: 'UpdateDepartment', dept_code:$scope.dept_code, dept_desc:$scope.dept_desc},
						function(result){
							if(result.results == 1){
								$scope.queryOrgData();
								
								}
						});
			}
			$scope.deleteOrgData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype, dept_code: null, dept_desc: null},
						{"a": 'DeleteDepartment', "dept_code": $scope.dept_code},
						function(result){
							if(result.results == 1){
								$scope.dept_code=null;
								$scope.dept_desc=null;
								$scope.queryOrgData();
								}
						});
			}
		}]
	}
});

myapp.service("resSet", ObjectiveResourceSetter)
.directive("objmngInputForm", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/objmng_input_form.html",
		scope:{
			submit: '&'
		},
		link: function(){
			jQuery(".btn").css({
				margin: "0px 8px 0px 0px"
			});
			jQuery(".input-form").css({
				margin: "10px 0px"
			});
		},
		controller: ['$scope','resSet', function($scope, resSet){
			$scope.querytype = "object";
			$scope.results = '';
			$scope.obj_priority = '';
			$scope.obj_code = '';
			$scope.obj_desc = '';
			$scope.queryObjData = function(){
				jQuery('.juiobjtable').css({
					display:"none"
				});
			resSet.ServerUrl.get({querytype: $scope.querytype, obj_code: null, obj_desc: null, obj_priority:null},
					function(results, responseHeader){
							angular.copy(results, $scope.results);
							if($scope.obj_code == '')
								$scope.submit({datas:results});
							else{
								var arrays = [];
								var element;
								while(results.results.length != 0){
									element  = results.results.pop();
									if(element.obj_code == $scope.obj_code)
										arrays.push(element);
								}
								dataObj = {results: arrays}
								$scope.submit({datas:dataObj});
								$scope.obj_code = '';
								$scope.obj_desc = '';
								$scope.obj_priority = '';
							}
						}
					);
			}
			$scope.saveObjData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype},
						{'a': 'CreateObject', 'obj_code':$scope.obj_code, 'obj_desc':$scope.obj_desc, 'obj_priority':$scope.obj_priority},
						function(result){
							if(result.results == 1)
								$scope.queryObjData();
						});
			}
			$scope.updateObjData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype, obj_code: null, obj_desc: null, obj_priority:null},
						{'a': 'UpdateObject', 'obj_code':$scope.obj_code, 'obj_desc': $scope.obj_desc, 'obj_priority':$scope.obj_priority},
						function(result){
							if(result.results == 1){
								$scope.queryObjData();
								
								}
						});
			}
			$scope.deleteObjData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype, obj_code: null, obj_desc: null, obj_priority:null},
						{'a': 'DeleteObject', 'obj_code': $scope.obj_code},
						function(result){
							if(result.results == 1){
								$scope.obj_code = null;
								$scope.obj_desc = null;
								$scope.obj_priority = null;
								$scope.queryObjData();
								}
						});
			}
		}]
	}
});

myapp.service("resSet", OranizationObjectiveResourceSetter)
.directive("orgobjmngInputForm", function(){
	return {
		restrict: "EA",
		templateUrl: "../../html/template/orgobjmng_input_form.html",
		scope: {
			submit: '&'
		},
		link: function(){
			jQuery(".btn").css({
				margin: "0px 8px 0px 0px"
			});
			jQuery(".input-form").css({
				margin: "10px 0px"
			});
			jQuery(".checkbox").css({
				margin: "10px 26px 20px 0px"
			});
		},
		controller: ['$scope','resSet', function($scope, resSet){
			$scope.querytype = "dept-obj";
			$scope.dept_code = '';
			$scope.obj_code = '';
			$scope.obj_desc = ''
			$scope.dept_desc = ''
			$scope.results = '';
			$scope.queryOrgObjData = function(){
				console.log(castFromBooleanToString($scope.dept_obj_resp))
				console.log(typeof(castFromBooleanToString($scope.dept_obj_resp)))
				jQuery('.juiorgobjtable').css({
					display:"none"
				});
			resSet.ServerUrl.get({querytype: $scope.querytype, dept_code:null, obj_code:null, dept_obj_resp:null, dept_obj_auth:null, dept_obj_exp:null, dept_obj_work:null, dept_obj_ref:null},
					function(results, responseHeader){
							$scope.results = results;
							if($scope.obj_code == '' && $scope.obj_desc == '' && $scope.dept_code == '' && $scope.dept_desc == '')
								$scope.submit({datas:results});
							else{
								var arrays = [];
								var element;
								while(results.results.length != 0){
									element  = results.results.pop();
									if(element.obj_code == $scope.obj_code && element.dept_code == $scope.dept_code)
										arrays.push(element);
									else if($scope.obj_code=='' && element.dept_code == $scope.dept_code)
										arrays.push(element);
									else if($scope.dept_code=='' && element.obj_code == $scope.obj_code)
										arrays.push(element);
								}
								dataObj = {results: arrays}
								$scope.submit({datas:dataObj});
								$scope.dept_code = '';
								$scope.obj_code = '';
								$scope.dept_desc = '';
								$scope.obj_desc = '';
							}
						}
					);
			}
			$scope.saveOrgObjData = function(){
			$scope.dept_obj_resp = castFromBooleanToString($scope.dept_obj_resp);
			$scope.dept_obj_auth = castFromBooleanToString($scope.dept_obj_auth);
			$scope.dept_obj_exp = castFromBooleanToString($scope.dept_obj_exp);
			$scope.obj_work = castFromBooleanToString($scope.dept_obj_work);
			$scope.dept_obj_ref = castFromBooleanToString($scope.dept_obj_ref);
				resSet.ServerUrl.save({querytype: $scope.querytype, dobj_code: null, obj_desc: null, obj_priority:null},
						{'a': 'CreateDeptObj', 'dept_code':$scope.dept_code, 'obj_code':$scope.obj_code, 'dept_obj_resp':castFromBooleanToString($scope.dept_obj_resp), 'dept_obj_auth':castFromBooleanToString($scope.dept_obj_auth), 'dept_obj_exp':castFromBooleanToString($scope.dept_obj_exp), 'dept_obj_work':castFromBooleanToString($scope.dept_obj_work), 'dept_obj_ref':castFromBooleanToString($scope.dept_obj_ref)},
						function(result){
							if(result.results == 1)
								$scope.queryOrgObjData();	
						});
			}
			$scope.updateOrgObjData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype, obj_code: null, obj_desc: null, obj_priority:null},
						{'a': 'UpdateDeptObj', 'dept_code':$scope.dept_code, 'obj_code':$scope.obj_code, 'dept_obj_resp':'0', 'dept_obj_auth':'0', 'dept_obj_exp':'0', 'dept_obj_work':'0', 'dept_obj_ref':'0'},
						function(result){
							if(result.results == 1){
								$scope.queryOrgObjData();
								
								}
						});
			}
			$scope.deleteOrgObjData = function(){
				resSet.ServerUrl.save({querytype: $scope.querytype, obj_code: null, obj_desc: null, obj_priority: null},
						{'a': 'DeleteDeptObj', 'dept_code': $scope.dept_code, 'obj_code': $scope.obj_code},
						function(result){
							if(result.results == 1){
								$scope.obj_code='';
								$scope.obj_desc='';
								$scope.obj_priority='';
								$scope.queryOrgObjData();
								}
						});
			}
		}]
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
					jQuery(".table" + i).css({
						display:"none"
					})
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


//Defined Function

function castFromBooleanToString(arg){
	if(arg == false)
		return String(0);
	else if(arg == true)
		return String(1);
}

function filterResult(arg){
	if(arg == '')
		return null;
	else
		return arg;
}