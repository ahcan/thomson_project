app.controller('ctrl-thomson-HCM',function($scope, $http, $timeout, $window, $interval) {
// body...
    $scope.host = "thomson-hcm";
    $scope.isRealTime = false;
    $scope.isJob = false;
    $scope.node_id = 0;
    var tick = false;
    var tickAllLog = false;
    $scope.reloadNodes = function(){
        tick = false;
        $scope.$broadcast('loadNode-HCM');
        $http({
            method:"GET",
            url:"/system/api/"+$scope.host+"/nstatus/",
            timeout:2000,
        }).then(function(response){
            if(response.status == 200){
                $scope.lstNodes = response.data;
                tick = true;
            }
            $scope.$broadcast('uloadNode-HCM');
        }, function(response){tick = true; if (response.status == 401) {$window.location.href= '/accounts/login/';}});
    };
    //reload nodes
    $timeout(function() {$interval(function() {
        if(tick){$scope.reloadNodes();}
    }, 3000);}, 100);
    $scope.reloadJobs = function(){
        $http({
            method:'GET',
            url:"/job/api/"+$scope.host+"/count-job/",
        }).then(function(response){
            $scope.Jobs=response.data;
        });
    };
    $scope.reloadDevice = function(){
        $http({
            method:"GET",
            url:"/system/api/"+$scope.host+"/status/",
            timeout:3000,}).then(function(response){
            if(response.status == 200){
                $scope.PCStatus = response.data[0];
                $timeout(function() {
                $scope.reloadDevice();}, 3000);}
        }, function(){$timeout(function(){$scope.reloadDevice();}, 3000);});
    };
    $scope.show_detail = function(node_id) {
        // $window.location.href = '/system/detail-node/'+node_id+'/'
        $scope.lstLogJob = '';
        $scope.isRealTime = false;
        $scope.isJob = true;
        $timeout(function(){$scope.$broadcast('loadJob-HCM');},0);
        $http({
            method:'GET',
            url:'/system/api/'+$scope.host+'/'+node_id+'/',
        }).then(function(response){
            if($scope.nodeDetail == node_id){
                $scope.node = response.data[0];
                $scope.job_list = response.data[0].job_list;
                $scope.$broadcast('uloadJob-HCM');
            }
            // console.log($scope.job_list);
        });
        if ($scope.isJob && $scope.nodeDetail == node_id){
            $scope.reload_detail(node_id);
        }
        // console.log($scope.nodeDetail);
    };
    $scope.reload_detail = function(node_id){
        $scope.$broadcast('loadJob-HCM');
        $http({
            method:'GET',
            url:'/system/api/'+$scope.host+'/'+node_id+'/',
            timeou:700,
        }).then(function(response){
            if($scope.nodeDetail == node_id && response.status == 200){
                $scope.node = response.data[0];
                $scope.$broadcast('uloadJob-HCM');
                // $scope.job_list = response.data[0].job_list;
            }
        });
        if ($scope.isJob && $scope.nodeDetail == node_id){
            $timeout(function() {
                $scope.reload_detail(node_id);
            }, 3000);
        }
    };
    $scope.set_nodedatil = function(node_id){
        $scope.nodeDetail = node_id;
    };
    $scope.restartJob = function(job_id, node_id){
        if(angular.element(document.getElementById('cpt-value-widgetRestart1')).val()===""){
            alert("Please resolve the captcha and submit!");
        }else{
            $scope.$emit('loadMain-HCM');
            $http({
            method: 'PUT',
            url: '/job/api/' + $scope.host + '/' + job_id + '/restart/',
            }).then(function(response){
                if (response.status == 202) {
                    $window.alert('jod is started on node: '+response.data.message);
                    $scope.show_detail(node_id);
                    $scope.$emit('uloadMain-HCM');
                }
                else{
                    $scope.$emit('uloadMain-HCM');}
            });
        }
    };
    $scope.stopJob = function(job_id, node_id){
        if (angular.element(document.getElementById('cpt-value-widgetStop1')).val()===""){
            alert("Please resolve the captcha and submit!");
        }else{
            $scope.$emit('loadMain-HCM');
            $http({
            method: 'PUT',
            url: '/job/api/'+ $scope.host + '/'+job_id + '/abort/',
            }).then(function(response){
                if (response.status == 202) {
                $window.alert(response.data.message);
                $scope.show_detail(node_id);
                $scope.$emit('uloadMain-HCM');
                }
                else{$scope.emit('uloadMain-HCM');}
                });
        }
    };
    $scope.showLog = function(job_id, job_name){
        $scope.job_name = job_name;
        $scope.isRealTime = true;
        $scope.job_id = job_id;
        $timeout(function() { $scope.$broadcast('loadLog-HCM');}, 0);
        $http({
            method: 'GET',
            url: '/log/api/'+ $scope.host +'/'+ job_id +'/',
        }).then(function(response){
            if (response.status == 200){
                $scope.lstLogJob = response.data;
                // console.log(response.data);
                $scope.$broadcast('uloadLog-HCM');
            }else{
                console.log("Error");
                $scope.$broadcast('loadLog-HCM');
            }
        });
        $timeout(function(){$scope.reload_log(job_id, job_name);}, 10000);
    };
    $scope.reload_log = function(job_id, job_name){
        $scope.job_name = job_name;
        $timeout(function(){$scope.$broadcast('loadLog-HCM');}, 0);
        $http({
            method: 'GET',
            url: '/log/api/'+ $scope.host +'/'+ job_id +'/',
        }).then(function(response){
           if (response.status == 200 && $scope.job_id == job_id){
                $scope.lstLogJob = response.data;
                // console.log(response.data);
                $scope.$broadcast('uloadLog-HCM');
            }else{
                console.log("Error");
                $scope.$broadcast('loadLog-HCM');
            } 
        });
        if($scope.isJob && $scope.isRealTime && $scope.job_id == job_id){
            $timeout(function(){$scope.reload_log(job_id, job_name);}, 10000);
        }
    };
    $scope.loadAllLog = function(){
        tickAllLog = false;
        $scope.nowDate = +new Date();
        $scope.$broadcast('loadRealtime-HCM');
        $http({
            method: 'GET',
            url: '/log/api/'+$scope.host+'/log/',
            timeout:2000,
        }).then(function (response){
           if (response.status == 200) {
            tickAllLog = true;
            $scope.log_list = response.data;
            $scope.$broadcast('uloadRealtime-HCM');}
        }, function(response){tickAllLog = true;});
    };
    // reload All Log
    $timeout(function(){$interval(function(){if(tickAllLog && !$scope.isRealTime){$scope.loadAllLog();}},10000)}, 5000);
    $scope.checkBackup = function(job_id, node_id){
        $scope.job_id = job_id;
        $scope.node_id = node_id;
        $scope.txtHeader='Restart Job:&nbsp;'+job_id;
        $http({
            method: 'GET',
            url: '/job/api/' + $scope.host + '/' + job_id + '/check-backup/',
        }).then(function(response){
            if(response.status ==202){
                if(response.data[0]['backup']){
                    var tmp= "glyphicon glyphicon-ok";
                }else{ var tmp = "glyphicon glyphicon-remove";}
                var strbackup="<p>Define backup input:&nbsp;<i class=\""+tmp+"\"></i></p></br>";
                var strip = "<p>IP address:&nbsp;"+response.data[0]['ip']+"</p>";
                $scope.txtBody = strbackup+ strip;
            }
        });
    };
    $scope.dataModal = function(job_id, node_id){
        $scope.job_id = job_id;
        $scope.node_id = node_id;
        $scope.txtHeader = 'Stop Job:&nbsp;'+job_id;
        $http({
            method: 'GET',
            url: '/job/api/' + $scope.host + '/' + job_id + '/check-backup/',
        }).then(function(response){
            if(response.status ==202){
                if( response.data[0]['backup']){
                    var tmp= "glyphicon glyphicon-ok";
                }else{ var tmp = "glyphicon glyphicon-remove";}
                var strbackup="<p>Define backup input:&nbsp;<i class=\""+tmp+"\"></i></p></br>";
                var strip = "<p>IP address:&nbsp;"+response.data[0]['ip']+"</p>";
                $scope.txtBody = strbackup+ strip;
            }
        });
    };
    $scope.reverseSort = false;
    $scope.reloadDevice();
    $scope.reloadNodes();
    $scope.loadAllLog();
    $scope.reloadJobs();
});
$('#frm-modal-stop-thomson-hcm').submit(function() {
    if($('#cpt-value-widgetStop1').val()===""){
        $('#modal-stop-thomson-hcm').modal('show');
    }else{
        $('#modal-stop-thomson-hcm').modal('hide');
    }
    // console.log("####close###");
});
$('#frm-modal-restart-thomson-hcm').submit(function() {
    if($('#cpt-value-widgetRestart1').val()===""){
        $('#modal-restart-thomson-hcm').modal('show');
    }else{
        $('#modal-restart-thomson-hcm').modal('hide');
    }
});