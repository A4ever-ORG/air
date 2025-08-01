package cmd

import (
	"testing"
	"github.com/spf13/cobra"
)

func TestAddCommands(t *testing.T) {
	rootCmd := &cobra.Command{
		Use:   "test",
		Short: "Test command",
	}
	
	// Test that AddCommands doesn't panic
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("AddCommands panicked: %v", r)
		}
	}()
	
	AddCommands(rootCmd)
	
	// Check that commands were added
	commands := rootCmd.Commands()
	if len(commands) == 0 {
		t.Error("AddCommands should add at least one command")
	}
	
	// Check for expected commands
	expectedCommands := []string{"system", "network", "security", "install", "demo"}
	foundCommands := make(map[string]bool)
	
	for _, cmd := range commands {
		foundCommands[cmd.Use] = true
	}
	
	for _, expected := range expectedCommands {
		if !foundCommands[expected] {
			t.Errorf("Expected command '%s' not found", expected)
		}
	}
}

func TestSystemCommand(t *testing.T) {
	// Test that system command doesn't panic when executed
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("System command panicked: %v", r)
		}
	}()
	
	systemCmd.Run(systemCmd, []string{})
}

func TestNetworkCommand(t *testing.T) {
	// Test that network command doesn't panic when executed
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Network command panicked: %v", r)
		}
	}()
	
	networkCmd.Run(networkCmd, []string{})
}

func TestSecurityCommand(t *testing.T) {
	// Test that security command doesn't panic when executed
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Security command panicked: %v", r)
		}
	}()
	
	securityCmd.Run(securityCmd, []string{})
}

func TestInstallCommand(t *testing.T) {
	// Test that install command doesn't panic when executed
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Install command panicked: %v", r)
		}
	}()
	
	installCmd.Run(installCmd, []string{})
}

func TestDemoCommand(t *testing.T) {
	// Test that demo command doesn't panic when executed
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Demo command panicked: %v", r)
		}
	}()
	
	demoCmd.Run(demoCmd, []string{})
}