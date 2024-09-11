// TODO: Refactor my shit code, make google auth work

import { useState } from "react";
import Button from "./Button";

interface fieldProps {
  value: string;
  error: {
    status: boolean;
    message: string;
  };
}

function validateField(
  field: string,
  fieldType: "login" | "password" | "confirm",
  password: string | undefined = undefined
): fieldProps {
  const forbidden_login_symbols: Array<string> = [
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "-",
    "+",
    "=",
    "[",
    "]",
    "{",
    "}",
    "|",
    "\\",
    ":",
    ";",
    '"',
    "'",
    "<",
    ">",
    ",",
    ".",
    "?",
    "/",
  ];
  let status_value = false;
  let message = "";

  if (field.length === 0) {
    status_value = true;
    message = "Field is required";
  } else if (fieldType === "login") {
    if (field.length < 5) {
      status_value = true;
      message = "Too short!";
    } else if (field.length > 15) {
      status_value = true;
      message = "Too long!";
    } else {
      forbidden_login_symbols.forEach((symbol) => {
        if (field.includes(symbol)) {
          status_value = true;
          message = "No special symbols!";
        }
      });
    }
  } else if (fieldType === "password") {
    if (field.length > 30) {
      status_value = true;
      message = "Too long!";
    } else if (field.length < 6) {
      status_value = true;
      message = "Too short!";
    }
  } else {
    if (field !== password) {
      status_value = true;
      message = "check out your password again!";
    }
  }

  return {
    value: field,
    error: {
      status: status_value,
      message: message,
    },
  };
}

export default function Login() {
  const [login, setLogin] = useState<fieldProps>({
    value: "",
    error: {
      status: false,
      message: "",
    },
  });
  const [password, setPassword] = useState<fieldProps>({
    value: "",
    error: {
      status: false,
      message: "",
    },
  });

  const [confirm, setConfirm] = useState<fieldProps>({
    value: "",
    error: {
      status: false,
      message: "",
    },
  });

  const handleClick = () => {
    alert("Pretending to send the data to backend");
  };

  return (
    <form className="reg">
      <div className="field">
        <h3 className="text-left">Login</h3>
        <input
          className="input mt-1"
          type="text"
          id="login"
          onChange={(e) => {
            setLogin(validateField(e.target.value, "login"));
          }}
          required
        />{" "}
        {/*Without mt-1 "g" almost touches the input*/}
        <div className="h-6">
          <p className={login.error.status ? "error visible" : "invisible"}>
            {login.error.message}
          </p>
        </div>
      </div>

      <div className="field">
        <h3 className="text-left">Password</h3>
        <input
          className="input"
          type="password"
          id="password"
          onChange={(e) => {
            setPassword(validateField(e.target.value, "password"));
          }}
          required
        />
        <div className="h-6">
          <p className={password.error.status ? "error visible" : "invisible"}>
            {password.error.message}
          </p>
        </div>
      </div>

      <div className="field">
        <h3 className="text-left">Confirm password</h3>
        <input
          className="input mt-1"
          type="password"
          id="confirm"
          onChange={(e) => {
            setConfirm(
              validateField(e.target.value, "confirm", password.value)
            );
          }}
          required
        />
        <div className="h-6">
          <p className={confirm.error.status ? "error visible" : "invisible"}>
            {confirm.error.message}
          </p>
        </div>
      </div>

      <Button
        status={
          login.error.status ||
          password.error.status ||
          confirm.error.status ||
          !login.value ||
          !password.value ||
          !confirm.value
            ? "inactive"
            : "active"
        }
        onClick={handleClick}
      >
        Submit
      </Button>

      <p className="text-white text-xl">Or log in with:</p>

      <img
        src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"
        alt="Google"
        className="google-icon"
      />

      <p className="text-sm m-0">
        Other options <br /> coming soon...
      </p>
    </form>
  );
}
