import 'dart:convert';
import 'dart:io';
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/configs/app_config.dart';
import 'package:flutter_base/database/share_preferences_helper.dart';
import 'package:flutter_base/global/global_data.dart';
import 'package:flutter_base/helper/load_json_helper.dart';
import 'package:flutter_base/models/entities/farmer/farmer.dart';
import 'package:flutter_base/models/entities/farmer/farmer_detail_entity.dart';
import 'package:flutter_base/models/entities/garden/garden_entity.dart';
import 'package:flutter_base/models/entities/manager/manager_entity.dart';
import 'package:flutter_base/models/entities/process/list_process.dart';
import 'package:flutter_base/models/entities/tree/list_tree_response.dart';
import 'package:flutter_base/models/entities/user/user_entity.dart';
import 'package:flutter_base/models/entities/weather/weather_response.dart';
import 'package:flutter_base/models/enums/load_status.dart';
import 'package:flutter_base/repositories/auth_repository.dart';
import 'package:flutter_base/repositories/farmer_repository.dart';
import 'package:flutter_base/repositories/garden_repository.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/repositories/task_repository.dart';
import 'package:flutter_base/repositories/tree_repository.dart';
import 'package:flutter_base/repositories/user_repository.dart';
import 'package:flutter_base/repositories/weather_repository.dart';

import 'package:flutter_base/utils/logger.dart';

part 'app_state.dart';

class AppCubit extends Cubit<AppState> {
  TreeRepository treeRepository;
  GardenRepository gardenRepository;
  ProcessRepository processRepository;
  AuthRepository authRepository;
  TaskRepository taskRepository;
  UserRepository userRepository;
  FarmerRepository farmerRepository;
  WeatherRepository weatherRepository;
  AppCubit({
    required this.treeRepository,
    required this.authRepository,
    required this.processRepository,
    required this.gardenRepository,
    required this.taskRepository,
    required this.userRepository,
    required this.farmerRepository,
    required this.weatherRepository,
  }) : super(AppState());

  void getData() async {
    // await LoadJsonHelper.shared.load();
    fetchListGarden();
    fetchListProcess();
    fetchListTree();
    fetchListTask();
    fetchListManager();
    getListFarmerByManager();
    getWeather();
  }

  void fetchListTask() async {
    emit(state.copyWith(taskStatus: LoadStatus.LOADING));
    try {
      final result = await taskRepository.getListTask();
      emit(state.copyWith(
          tasks: result.data!.tasks, taskStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(taskStatus: LoadStatus.FAILURE));
    }
  }

  void fetchListManager() async {
    emit(state.copyWith(getManagersStatus: LoadStatus.LOADING));
    try {
      final response = await userRepository.getListManager();
      emit(state.copyWith(
          getManagersStatus: LoadStatus.SUCCESS,
          managers: response.data!.managers));
    } catch (e) {
      emit(state.copyWith(getManagersStatus: LoadStatus.FAILURE));
    }
  }

  void fetchListTree() async {
    emit(state.copyWith(getTreeStatus: LoadStatus.LOADING));
    try {
      final response = await treeRepository.getListTreeData();
      if (response != null) {
        emit(state.copyWith(
          getTreeStatus: LoadStatus.SUCCESS,
          trees: response.data!.trees,
        ));
      } else {
        emit(state.copyWith(getTreeStatus: LoadStatus.FAILURE));
      }
      emit(state.copyWith(getTreeStatus: LoadStatus.SUCCESS));
    } catch (error) {
      emit(state.copyWith(getTreeStatus: LoadStatus.FAILURE));
    }
  }

  void fetchListProcess() async {
    emit(state.copyWith(getProcessStatus: LoadStatus.LOADING));
    try {
      final response = await processRepository.getListProcessData();
      // if (response != null) {
      emit(state.copyWith(
        getProcessStatus: LoadStatus.SUCCESS,
        processes: response.data!.processes,
      ));
      // } else {
      //   emit(state.copyWith(getProcessStatus: LoadStatus.FAILURE));
      // }
      emit(state.copyWith(getProcessStatus: LoadStatus.SUCCESS));
    } catch (error) {
      emit(state.copyWith(getProcessStatus: LoadStatus.FAILURE));
    }
  }

  void fetchListGarden() async {
    emit(state.copyWith(getGardenStatus: LoadStatus.LOADING));
    try {
      final response = await gardenRepository.getGardenData();
      // if (response != null) {
      emit(state.copyWith(
        getGardenStatus: LoadStatus.SUCCESS,
        gardens: response.data!.gardens,
      ));
      // } else {
      //   emit(state.copyWith(getGardenStatus: LoadStatus.FAILURE));
      // }
      emit(state.copyWith(getGardenStatus: LoadStatus.SUCCESS));
    } catch (error) {
      emit(state.copyWith(getGardenStatus: LoadStatus.FAILURE));
    }
  }

  void removeUserSection() {
    authRepository.removeToken();
    GlobalData.instance.token = null;
  }

  void getListFarmerByManager() async {
    emit(state.copyWith(farmerStatus: LoadStatus.LOADING));
    try {
      final FarmerList result = await farmerRepository
          .getListFarmerByManager(GlobalData.instance.userEntity!.id);
      emit(state.copyWith(
          farmers: result.data!.farmers, farmerStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(farmerStatus: LoadStatus.FAILURE));
    }
  }

  void getWeather() async {
    String? longitude = await SharedPreferencesHelper.getLongitude();
    String? latitude = await SharedPreferencesHelper.getLatitude();

    print('longitude $longitude');
    print('latitude $latitude');

    emit(state.copyWith(weatherStatus: LoadStatus.LOADING));
    try {
      final response = await weatherRepository.getCurrentWeather(
          latitude!, longitude!, AppConfig.apiKey);
      emit(
          state.copyWith(weather: response, weatherStatus: LoadStatus.SUCCESS));
    } catch (e) {
      emit(state.copyWith(weatherStatus: LoadStatus.FAILURE));
    }
  }

  // void getProfile() async {
  //   emit(state.copyWith(fetchUser: LoadStatus.LOADING));
  //   try {
  //     final userRes = await userRepository.getProfile();
  //
  //     emit(state.copyWith(user: userRes));
  //
  //     emit(state.copyWith(fetchUser: LoadStatus.SUCCESS));
  //   } catch (error) {
  //     logger.e(error);
  //     emit(state.copyWith(fetchUser: LoadStatus.FAILURE));
  //   }
  // }
  // ///Sign Out
  // void signOut() async {
  //   emit(state.copyWith(signOutStatus: LoadStatus.LOADING));
  //   try {
  //     final deviceToken = await FirebaseMessaging.instance.getToken();
  //     final param = SignOutParam(deviceToken: deviceToken);
  //     //Todo
  //     await authRepository.signOut(param);
  //     await FirebaseMessaging.instance.deleteToken();
  //     await authRepository.removeToken();
  //     GlobalData.instance.token = null;
  //     AppState newState = state.copyWith(signOutStatus: LoadStatus.SUCCESS);
  //     newState.user = null;
  //     emit(newState);
  //   } catch (e) {
  //     logger.e(e);
  //     emit(state.copyWith(signOutStatus: LoadStatus.FAILURE));
  //   }
  // }
}
