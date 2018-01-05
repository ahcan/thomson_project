app.controller('ctrl-thomson-HCM',function($scope, $http, $timeout, $window, $interval) {
// body...
    $scope.host = "thomson-hcm";
    $scope.isRealTime = false;
    $scope.isJob = false;
    $scope.node_id = 0;
    // $scope.isLoad = true;
    $scope.reloadNodes = function(){
        $timeout(function() { $scope.$broadcast('loadNode-HCM');}, 0);
        $http.get("/system/api/"+$scope.host+"/nstatus/").then(function(reponse){
            $scope.lstNodes = reponse.data;
            $scope.$broadcast('uloadNode-HCM');
            // console.log(data);
        });
        $timeout(function() {
            $scope.reloadNodes();
        }, 3000)
    };
    $scope.reloadJobs = function(){
        $http({
            method:'GET',
            url:"/job/api/"+$scope.host+"/count-job/",
        }).then(function(response){
            $scope.Jobs=response.data;
        });
    }
    $scope.reloadDevice = function(){
        $http.get("/system/api/"+$scope.host+"/status/").then(function(reponse){
            $scope.PCStatus = reponse.data[0];
        });
        $timeout(function() {
            $scope.reloadDevice();
        }, 3000)
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
        $timeout(function(){$scope.$broadcast('loadJob-HCM');},0);
        $http({
            method:'GET',
            url:'/system/api/'+$scope.host+'/'+node_id+'/',
        }).then(function(response){
            if($scope.nodeDetail == node_id){
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
        if($window.confirm("Confirm Retart Job: "+job_id)){
            $http({
            method: 'PUT',
            url: '/job/api/' + $scope.host + '/' + job_id + '/restart/',
            }).then(function(response){
                if (response.status == 202) {
                    $window.alert(response.data.message);
                    $scope.show_detail(node_id);
                }
            });
        }
    };
    $scope.stopJob = function(job_id, node_id){
        if($window.confirm("Confirm Stop Job: "+job_id)){
            $http({
            method: 'PUT',
            url: '/job/api/'+ $scope.host + '/'+job_id + '/abort/',
            }).then(function(response){
                if (response.status == 202) {
                $window.alert(response.data.message);
                $scope.show_detail(node_id);
                }
            });
        }
    };
    $scope.showLog = function(job_id, job_name){
        $scope.job_name = job_name;
        $scope.isRealTime = true;
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
           if (response.status == 200){
                $scope.lstLogJob = response.data;
                // console.log(response.data);
                $scope.$broadcast('uloadLog-HCM');
            }else{
                console.log("Error");
                $scope.$broadcast('loadLog-HCM');
            } 
        });
        if($scope.isJob && $scope.isRealTime){
            $timeout(function(){$scope.reload_log(job_id, job_name);}, 10000);
        }
    };
    $scope.loadAllLog = function(){
        $scope.nowDate = +new Date();
        $timeout(function() { $scope.$broadcast('loadRealtime-HCM');}, 0);
        $http({
            method: 'GET',
            url: '/log/api/'+$scope.host+'/log/',
        }).then(function (response){
            $scope.log_list = response.data;
            $scope.$broadcast('uloadRealtime-HCM');
        });
        if (!$scope.isRealTime) {
            $timeout(function(){$scope.loadAllLog();}, 10000);
        }
    };
    $scope.reverseSort = false;
    $scope.reloadDevice();
    $scope.reloadNodes();
    $scope.loadAllLog();
    $scope.reloadJobs();
});