part of 'login_cubit.dart';

enum LoginStatusBagri {
  INITIAL,
  LOADING,
  SUCCESS,
  FAILURE,
  USERNAME_PASSWORD_INVALID,
}

class LoginState extends Equatable {
  final LoginStatusBagri LoginStatus;
  final String username;
  final String password;
  final RoleEntity? role;

  LoginState(
      {this.LoginStatus = LoginStatusBagri.INITIAL,
      this.username = "",
      this.password = "",
      this.role});

  bool get isValid {
    if (isValidEmail || isValidPhone) {
      return true;
    } else {
      return false;
    }
  }

  bool get isValidEmail {
    return Validator.validateEmail(username);
  }

  bool get isValidPhone {
    return Validator.validatePhone(username);
  }

  LoginState copyWith({
    LoginStatusBagri? LoginStatus,
    String? username,
    String? password,
    RoleEntity? role,
  }) {
    return new LoginState(
      LoginStatus: LoginStatus ?? this.LoginStatus,
      username: username ?? this.username,
      password: password ?? this.password,
      role: role ?? this.role,
    );
  }

  @override
  List<Object?> get props => [
        this.LoginStatus,
        this.username,
        this.password,
        this.role,
      ];
}
