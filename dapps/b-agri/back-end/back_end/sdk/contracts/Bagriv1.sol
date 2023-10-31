// SPDX-License-Identifier: UNLICENSED
pragma experimental ABIEncoderV2;

pragma solidity ^0.8.3;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract Bagriv1 is Initializable {
    bool _active;
    address _owner;

    modifier checkStatus() {
        require(_active, "Smart contract is not active");
        _;
    }

    modifier checkOwner() {
        require(msg.sender==_owner, "Permission require");
        _;
    }
    

    struct Season{
        string season_id;
        string processes;
        string start_date;
        string end_date;
        string name;
        string garden_id;
        string[] task_ids;
        string tree_id;
    }
    mapping(string => Season) seasons;

    struct Garden{
        string garden_id;
        string name;
        string area;
        string season_id;
    }
    mapping(string => Garden) gardens;

    struct Task{
        string task_id;
        string name;
        string description;
        string date;
        string start_time;
        string end_time;
        string results;
        string season_id;
        string[] farmer_ids;
    }
    mapping(string => Task) tasks;

    struct Farmer{
        string farmer_id;
        string name;
        string task_id;
    }
    mapping(string => Farmer) farmers;

    struct Tree{
        string tree_id;
        string name;
        string description;
        string season_id;
    }
    mapping(string => Tree) trees;

    function getSeason(
        string memory season_id) checkStatus public view returns(Season memory){
        Season storage _season = seasons[season_id];
        return (_season);
    }
    function createSeason(Season memory season) checkStatus public {
        Season storage _season = seasons[season.season_id];
        _season.season_id = season.season_id;
        _season.processes = season.processes;
        _season.start_date = season.start_date;
        _season.end_date = season.end_date;
        _season.name = season.name;
        _season.garden_id = season.garden_id;
        _season.task_ids = season.task_ids;
        _season.tree_id = season.tree_id;
    }    
    function updateSeason(Season memory season) checkStatus public {
        Season storage _season = seasons[season.season_id];
        _season.season_id = season.season_id;
        _season.processes = season.processes;
        _season.start_date = season.start_date;
        _season.end_date = season.end_date;
        _season.name = season.name;
        _season.garden_id = season.garden_id;
        _season.task_ids = season.task_ids;
        _season.tree_id = season.tree_id;
    }    
    function getGarden(
        string memory garden_id) checkStatus public view returns(Garden memory){
        Garden storage _garden = gardens[garden_id];
        return (_garden);
    }
    function createGarden(Garden memory garden) checkStatus public {
        Garden storage _garden = gardens[garden.garden_id];
        _garden.garden_id = garden.garden_id;
        _garden.name = garden.name;
        _garden.area = garden.area;
        _garden.season_id = garden.season_id;
    }    
    function updateGarden(Garden memory garden) checkStatus public {
        Garden storage _garden = gardens[garden.garden_id];
        _garden.garden_id = garden.garden_id;
        _garden.name = garden.name;
        _garden.area = garden.area;
        _garden.season_id = garden.season_id;
    }    
    function getTask(
        string memory task_id) checkStatus public view returns(Task memory){
        Task storage _task = tasks[task_id];
        return (_task);
    }
    function createTask(Task memory task) checkStatus public {
        Task storage _task = tasks[task.task_id];
        _task.task_id = task.task_id;
        _task.name = task.name;
        _task.description = task.description;
        _task.date = task.date;
        _task.start_time = task.start_time;
        _task.end_time = task.end_time;
        _task.results = task.results;
        _task.season_id = task.season_id;
        _task.farmer_ids = task.farmer_ids;
    }    
    function updateTask(Task memory task) checkStatus public {
        Task storage _task = tasks[task.task_id];
        _task.task_id = task.task_id;
        _task.name = task.name;
        _task.description = task.description;
        _task.date = task.date;
        _task.start_time = task.start_time;
        _task.end_time = task.end_time;
        _task.results = task.results;
        _task.season_id = task.season_id;
        _task.farmer_ids = task.farmer_ids;
    }    
    function getFarmer(
        string memory farmer_id) checkStatus public view returns(Farmer memory){
        Farmer storage _farmer = farmers[farmer_id];
        return (_farmer);
    }
    function createFarmer(Farmer memory farmer) checkStatus public {
        Farmer storage _farmer = farmers[farmer.farmer_id];
        _farmer.farmer_id = farmer.farmer_id;
        _farmer.name = farmer.name;
        _farmer.task_id = farmer.task_id;
    }    
    function updateFarmer(Farmer memory farmer) checkStatus public {
        Farmer storage _farmer = farmers[farmer.farmer_id];
        _farmer.farmer_id = farmer.farmer_id;
        _farmer.name = farmer.name;
        _farmer.task_id = farmer.task_id;
    }    
    function getTree(
        string memory tree_id) checkStatus public view returns(Tree memory){
        Tree storage _tree = trees[tree_id];
        return (_tree);
    }
    function createTree(Tree memory tree) checkStatus public {
        Tree storage _tree = trees[tree.tree_id];
        _tree.tree_id = tree.tree_id;
        _tree.name = tree.name;
        _tree.description = tree.description;
        _tree.season_id = tree.season_id;
    }    
    function updateTree(Tree memory tree) checkStatus public {
        Tree storage _tree = trees[tree.tree_id];
        _tree.tree_id = tree.tree_id;
        _tree.name = tree.name;
        _tree.description = tree.description;
        _tree.season_id = tree.season_id;
    }    

    function initialize() public initializer {
        _active = true;
        _owner = msg.sender;
    }

    function getStatus() public view returns(bool) {
        return _active;
    }

    function setStatus(bool active) checkOwner public {
        _active = active;
    }
}