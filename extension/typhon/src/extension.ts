// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "typhon" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('typhon.open', () => {
		// The code you place here will be executed every time your comma end is executed
		vscode.window.showInformationMessage('Hello World from Typhon!');
	});

	context.subscriptions.push(disposable);

	context.subscriptions.push(
		vscode.commands.registerCommand('typhon.test', () => {
			vscode.commands.executeCommand('editor.action.selectAll').then(() =>{
				// vscode.commands.executeCommand('editor.action.clipboardCopyAction').then(() =>{
				// 	vscode.commands.executeCommand('workbench.action.closeActiveEditor').then(() =>{
				// 		vscode.commands.executeCommand('workbench.action.files.newUntitledFile').then(() =>{
				// 			vscode.commands.executeCommand('editor.action.clipboardPasteAction');
				// 		});
				// 	});
				// });

				const editor = vscode.window.activeTextEditor;
				if (editor) {
					// Get whole text in editor
					console.log(editor.document.getText());
				}
			});
		}
	));
}

// This method is called when your extension is deactivated
export function deactivate() {}
