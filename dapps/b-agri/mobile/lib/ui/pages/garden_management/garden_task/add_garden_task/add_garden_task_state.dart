part of 'add_garden_task_cubit.dart';

class AddGardenTaskState extends Equatable {
  StepEntity? step;
  String? name;
  String? description;
  String? manager_id;
  String? season_id;
  String? date;
  String? start_time;
  String? end_time;
  List<String>? result;
  String? startHour;
  String? startMinute;
  String? endHour;
  String? endMinute;
  String? items;

  List<FarmerEntity>? farmers;
  LoadStatus? addGardenTaskStatus;
  List<FileEntity>? files;
  LoadStatus? uploadFileStatus;
  LoadStatus? removeFileStatus;

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
        this.startHour,
        this.startMinute,
        this.endHour,
        this.endMinute,
        this.farmers,
        this.items,
        this.addGardenTaskStatus,
        this.uploadFileStatus,
        this.files,
        this.removeFileStatus,
      ];

  AddGardenTaskState({
    this.step,
    this.name,
    this.description,
    this.manager_id,
    this.season_id,
    this.date,
    this.start_time,
    this.end_time,
    this.result,
    this.startHour,
    this.startMinute,
    this.endHour,
    this.endMinute,
    this.farmers,
    this.items,
    this.files,
    this.addGardenTaskStatus,
    this.uploadFileStatus,
    this.removeFileStatus,
  });

  AddGardenTaskState copyWith({
    StepEntity? step,
    String? name,
    String? description,
    String? manager_id,
    String? season_id,
    String? date,
    String? start_time,
    String? end_time,
    List<String>? result,
    String? startHour,
    String? startMinute,
    String? endHour,
    String? endMinute,
    List<FarmerEntity>? farmers,
    String? items,
    LoadStatus? addGardenTaskStatus,
    List<FileEntity>? files,
    LoadStatus? uploadFileStatus,
    LoadStatus? removeFileStatus,
  }) {
    return AddGardenTaskState(
      step: step ?? this.step,
      name: name ?? this.name,
      description: description ?? this.description,
      manager_id: manager_id ?? this.manager_id,
      season_id: season_id ?? this.season_id,
      date: date ?? this.date,
      start_time: start_time ?? this.start_time,
      end_time: end_time ?? this.end_time,
      result: result ?? this.result,
      startHour: startHour ?? this.startHour,
      startMinute: startMinute ?? this.startMinute,
      endHour: endHour ?? this.endHour,
      endMinute: endMinute ?? this.endMinute,
      farmers: farmers ?? this.farmers,
      files: files ?? this.files,
      items: items ?? this.items,
      addGardenTaskStatus: addGardenTaskStatus ?? this.addGardenTaskStatus,
      uploadFileStatus: uploadFileStatus ?? this.uploadFileStatus,
      removeFileStatus: removeFileStatus ?? this.removeFileStatus,
    );
  }
}
