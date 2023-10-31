part of 'update_garden_task_cubit.dart';

class UpdateGardenTaskState extends Equatable {
  StepEntity? step;
  String? name;
  String? description;
  String? manager_id;
  String? season_id;
  String? date;
  String? start_time;
  String? end_time;
  List<String>? result;
  List<FarmerEntity>? farmers;
  String? startHour;
  String? startMinute;
  String? endHour;
  String? endMinute;
  LoadStatus? updateGardenTaskStatus;
  LoadStatus? loadDetailStatus;
  List<FileEntity>? files;
  LoadStatus? uploadFileStatus;
  LoadStatus? removeFileStatus;
  String? items;

  @override
  List<Object?> get props => [
        this.step,
        this.name,
        this.description,
        this.manager_id,
        this.season_id,
        this.date,
        this.start_time,
        this.end_time,
        this.result,
        this.farmers,
        this.startHour,
        this.startMinute,
        this.endHour,
        this.endMinute,
        this.loadDetailStatus,
        this.updateGardenTaskStatus,
        this.uploadFileStatus,
        this.files,
        this.removeFileStatus,
        this.items,
      ];

  UpdateGardenTaskState({
    this.step,
    this.name,
    this.description,
    this.manager_id,
    this.season_id,
    this.date,
    this.start_time,
    this.end_time,
    this.result,
    this.farmers,
    this.startHour,
    this.startMinute,
    this.endHour,
    this.endMinute,
    this.updateGardenTaskStatus,
    this.loadDetailStatus,
    this.files,
    this.uploadFileStatus,
    this.removeFileStatus,
    this.items,
  });

  UpdateGardenTaskState copyWith({
    StepEntity? step,
    String? name,
    String? description,
    String? manager_id,
    String? season_id,
    String? date,
    String? start_time,
    String? end_time,
    List<String>? result,
    List<FarmerEntity>? farmers,
    String? startHour,
    String? startMinute,
    String? endHour,
    String? endMinute,
    LoadStatus? updateGardenTaskStatus,
    LoadStatus? loadDetailStatus,
    List<FileEntity>? files,
    LoadStatus? uploadFileStatus,
    LoadStatus? removeFileStatus,
    String? items,
  }) {
    return UpdateGardenTaskState(
      step: step ?? this.step,
      name: name ?? this.name,
      description: description ?? this.description,
      manager_id: manager_id ?? this.manager_id,
      season_id: season_id ?? this.season_id,
      date: date ?? this.date,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      result: result ?? this.result,
      farmers: farmers ?? this.farmers,
      startHour: startHour ?? this.startHour,
      startMinute: startMinute ?? this.startMinute,
      endHour: endHour ?? this.endHour,
      endMinute: endMinute ?? this.endMinute,
      updateGardenTaskStatus:
          updateGardenTaskStatus ?? this.updateGardenTaskStatus,
      loadDetailStatus: loadDetailStatus ?? this.loadDetailStatus,
      files: files ?? this.files,
      uploadFileStatus: uploadFileStatus ?? this.uploadFileStatus,
      removeFileStatus: removeFileStatus ?? this.removeFileStatus,
      items: items ?? this.items,
    );
  }
}
