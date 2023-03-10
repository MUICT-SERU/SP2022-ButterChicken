import * as vscode from "vscode";
import { runTyphon } from "./typhon";

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  console.log("Typhon extension activated");

  const commandConfigs = [
    {
      command: "typhon.run.normal",
      isPreProcessed: false,
      isSideFeature: false,
      mlSupport: true,
    },
    {
      command: "typhon.run.preProcess",
      isPreProcessed: true,
      isSideFeature: false,
      mlSupport: false,
    },
    {
      command: "typhon.run.side",
      isPreProcessed: false,
      isSideFeature: true,
      mlSupport: true,
    },
  ];

  commandConfigs.map((config) =>
    context.subscriptions.push(
      vscode.commands.registerCommand(config.command, () =>
        runTyphon({
          isPreProcessed: config.isPreProcessed,
          isSideFeature: config.isSideFeature,
          mlSupport: config.mlSupport,
        })
      )
    )
  );
}

// This method is called when your extension is deactivated
export function deactivate() {}
